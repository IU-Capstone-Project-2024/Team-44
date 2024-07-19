from ast import Dict
import asyncio
import os
import uuid
from contextlib import asynccontextmanager
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from redis.asyncio import Redis
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from .lang_graph.QuizGenerator import QuizGenerator
from .lang_graph.SummaryGenerator import SummaryGenerator
from .lang_graph.ValidationModels import Question, Quiz, Summary

# Configuration
load_dotenv()

API_KEY_NAME = os.getenv("API_KEY", "api_key")
API_KEY = os.getenv("API_KEY", "api_key")
MAX_QUEUE_SIZE = int(os.getenv("MAX_QUEUE_SIZE", 20))
RATE_LIMIT = os.getenv("RATE_LIMIT", 100)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "quiz_db")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info(
            "\n\n\tStarting up, attempting to connect to Quiz and Summary generators."
        )
        global quiz_generator, summary_generator
        quiz_generator = QuizGenerator()
        summary_generator = SummaryGenerator()
        logger.info("\tConnected to Quiz and Summary generators successfully.\n")
        logger.info("\tAttempting to connect to Redis and MongoDB.")
        global redis, mongo_client, db
        redis = Redis.from_url(REDIS_URL, decode_responses=True)
        mongo_client = AsyncIOMotorClient(MONGO_URL)
        db = mongo_client[MONGO_DB]

        logger.info("\tConnected to Redis and MongoDB successfully.\n\n")

        logger.info("Processing pending requests in the queue.")
        while await redis.llen("request_queue") > 0:
            request_id = await redis.lpop("request_queue")
            if request_id:
                logger.info(f"Processing pending request: {request_id}")
                await process_request(request_id)
        yield
    except Exception as e:
        logger.error(f"An error occurred during startup: {e}")
        raise
    finally:
        try:
            logger.info("Shutting down, performing cleanup tasks.")
            if redis:
                await redis.close()
            if mongo_client:
                await mongo_client.close()
            logger.info("Cleanup completed.")
        except Exception as e:
            logger.error(f"An error occurred during shutdown: {e}")


app = FastAPI(lifespan=lifespan)

redis = Redis.from_url(REDIS_URL, decode_responses=True)
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client[MONGO_DB]

request_queue = asyncio.Queue(maxsize=MAX_QUEUE_SIZE)

# API Key Header
api_key_header = APIKeyHeader(name=API_KEY_NAME)

class TextRequest(BaseModel):
    text: List[str]


async def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )


@app.post("/summary", response_model=Summary)
async def summary(
    request: TextRequest,
    api_key: str = Depends(get_api_key),
) -> Summary:
    return summary_generator.generate_summary(request.text)

@app.post("/quiz")
# @limiter.limit(RATE_LIMIT)
async def quiz(
    request: TextRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(get_api_key),
) -> dict:
    logger.info("\nReceived quiz generation request.")
    if await redis.llen("request_queue") >= MAX_QUEUE_SIZE:
        logger.warning("Service is busy. Rejecting request.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is currently busy. Please try again later.",
        )

    request_id = str(uuid.uuid4())
    await redis.rpush("request_queue", request_id)

    logger.info(f"Request {request_id} regestred.")
    await redis.set(request_id, request.model_dump_json())

    logger.info(f"Request {request_id} is being processed.")
    background_tasks.add_task(process_request, request_id)

    return {"detail": "Your request is being processed.", "request_id": request_id}


async def process_request(request_id: str):
    logger.info(f"\nProcessing request {request_id}.")

    request_data = await redis.get(request_id)
    if request_data is None:
        logger.warning(f"Request {request_id} not found in Redis.")
        return
    
    request = TextRequest.model_validate_json(request_data)
    #quiz = quiz_generator.generate_pquiz(chunks=request.text)
    quiz = await quiz_generator.generate_quiz_abatch(chunks=request.text)
    await db.quizzes.insert_one({"request_id": request_id, "quiz": quiz.model_dump_json()})
    await redis.delete(request_id)

    logger.info(f"Request {request_id} processed and saved to database.")


@app.get("/quiz/{request_id}", response_model=Quiz)
async def get_quiz_result(request_id: str):
    logger.info(f"\nFetching result for request {request_id}.")

    result = await db.quizzes.find_one({"request_id": request_id})
    if not result:
        logger.warning(f"Result for request {request_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Result not found."
        )
    else:
        await db.quizzes.delete_one({"request_id": request_id})
        logger.info(f"Result for request {request_id} returned and deleted from database.")
        return Quiz.model_validate_json(result["quiz"])
