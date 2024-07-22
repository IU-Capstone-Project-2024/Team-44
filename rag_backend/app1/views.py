from django.http import StreamingHttpResponse
from .serializers import SummarySerializer, QuizSerializer, TextSerializer
from rest_framework import status
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import JsonResponse

# from fastapi_ml.app.lang_graph.router import Router
from django.views.decorators.csrf import csrf_exempt
from requests.exceptions import RequestException
from django.views.decorators.csrf import csrf_exempt
from time import sleep
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from rag_backend import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from base64 import urlsafe_b64encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from semantic_chunkers import StatisticalChunker
from VectorSpace.Embedder import Embedder
import json

import asyncio
import aiohttp

import logging 
from pymongo import MongoClient 
import redis 

from typing import List


async def generate_summary(text):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:8080/summary",
            json={"text": text},
            headers={"api_key": "api_key"},
        ) as response:
            data = await response.json()
            return data


# async def generate_quiz(session, query):
#     async with session.post('http://localhost:8080/quiz', json={'query': query}) as response:
#         return await response.json()

text_splitter = StatisticalChunker(
    encoder=Embedder(),
    name="statistical_chunker",
    threshold_adjustment=0.01,
    dynamic_threshold=True,
    window_size=5,
    min_split_tokens=100,
    max_split_tokens=500,
    split_tokens_tolerance=10,
    plot_chunks=False,
    enable_statistics=False,
)


class SSEView(APIView):
    def get(self, request):
        def event_stream():
            for i in range(10):
                sleep(1)
                question = {"question": "What is 2 + 2?", "choices": ["3", "4", "5"]}
                yield f"data: {json.dumps(question)}\n\n"

        response = StreamingHttpResponse(
            event_stream(), content_type="text/event-stream"
        )
        return response

logger = logging.getLogger(__name__)

# MongoDB setup
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client.quiz_database
collection = db.quizzes

# Redis setup
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


class ReceiveQuizView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            quiz = data.get('quiz')
            token = request.headers.get('token')
            api_key = request.headers.get('api_key')
            
            # Validate token_id and api_key
            if not token or not api_key:
                logger.error("Missing token_id or api_key in headers.")
                return Response({"error": "Missing token_id or api_key in headers."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Save to MongoDB
            collection.insert_one({"token": token, "quiz": quiz})
            
            # Save to Redis
            redis_client.set(token, quiz)

            # Respond with a success message
            logger.info(f"Received quiz: {quiz}")
            return Response({"message": "Quiz received successfully."}, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            logger.error("Invalid JSON received.")
            return Response({"error": "Invalid JSON received."}, status=status.HTTP_400_BAD_REQUEST)

class SummaryView(APIView):
    def post(self, request, format=None):
        serializer = SummarySerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data["query"]

            chunks = text_splitter(docs=[query])[0]
            summaries = []
            for i in range(0, len(chunks), 2):
                print(len(chunks))
                batch_chunks = chunks[i : i + 2]
                for batch_chunk in batch_chunks:
                    print([" ".join(batch_chunk.splits)])
                    summary = asyncio.run(
                        generate_summary([" ".join(batch_chunk.splits)])
                    )
                    print(summary)
                    summaries.append(summary)
            return Response(summaries)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TimerView(APIView):
    def post(self, request, format=None):
        serializer = TextSerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data["text"]
            for i in range(10):
                print(i, query)

            return Response(query)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizView(APIView):
    def post(self, request, format=None):
        def event_stream(chunks: List[str]):
            for i in range(0, len(chunks), 2):
                batch_chunks = chunks[i : i + 2]
                data = {
                    "text": [
                        " ".join(batch_chunk.splits) for batch_chunk in batch_chunks
                    ]
                }
                quiz_token = requests.post(
                    "http://localhost:8080/quiz/",
                    json=data,
                    headers={"api_key": "api_key"},
                )
                sleep(4)
                waiting_for_gen = True
                while waiting_for_gen:
                    quiz = requests.get(
                        f'http://localhost:8080/quiz/{quiz_token.json()["request_id"]}',
                        headers={"api_key": "api_key"},
                    )
                    if quiz.status_code == 404:
                        sleep(4)
                    else:
                        print(quiz, quiz.json())
                        waiting_for_gen = False
                        yield quiz

        serializer = TextSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data["text"]

            chunks = text_splitter(docs=[text])[0]

            response = StreamingHttpResponse(
                event_stream(chunks), content_type="text/event-stream"
            )
            return response

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def main(request):
    return render(request, "main.html")
