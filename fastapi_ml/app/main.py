import asyncio
import json
from typing import List

from fastapi import Depends, FastAPI, HTTPException, WebSocket, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from lang_graph.agents.ValidationModels import Question
from lang_graph.router import Router
from langchain.text_splitter import (CharacterTextSplitter,
                                     RecursiveCharacterTextSplitter,
                                     TextSplitter)
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from pydantic import BaseModel

router = Router()
app = FastAPI()


class TextRequest(BaseModel):
    text: str


class QuestionModel(BaseModel):
    question: str
    options: List[str]
    correct_answers: List[str]


class QuizModel(BaseModel):
    questions: List[QuestionModel]


class SummaryRequest(BaseModel):
    query: str


@app.post("/summary")
async def summary(request: SummaryRequest):
    # if not request.user.is_authenticated:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not logged in")

    text_splitter = RecursiveCharacterTextSplitter()
    texts = text_splitter.create_documents([request.query])
    summary = router.generate_summary(texts)

    response_data = {
        'summary': summary,
    }
    return JSONResponse(content=response_data)


async def generate_summary_async(texts):
    summary = ""
    async with WebSocket.connect("ws://localhost:8000/ws/summary") as websocket:
        await websocket.send_text(json.dumps({"texts": texts}))
        while True:
            data = await websocket.receive_text()
            if data == "DONE":
                break
            summary += data + " "
    return summary


@app.websocket("/ws/summary")
async def websocket_summary(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        data = json.loads(data)
        texts = data["texts"]
        for word in router.generate_summary_words(texts):
            await websocket.send_text(word)
        await websocket.send_text("DONE")


@app.post("/quiz", response_model=QuizModel)
async def quiz(request: TextRequest):
    # if not request.user.is_authenticated:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not logged in")

    text_splitter = RecursiveCharacterTextSplitter()
    text = text_splitter.create_documents([request.text])
    quiz_json = router.generate_quiz(text)

    quiz_model = QuizModel(
        questions=[
            QuestionModel(
                question=question.question,
                options=question.options,
                correct_answers=question.correct_answers,
            )
            for question in quiz_json.questions
        ]
    )

    return quiz_model
