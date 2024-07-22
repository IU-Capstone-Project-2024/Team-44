import asyncio
import json
import os
from base64 import urlsafe_b64encode
from time import sleep
from uuid import uuid4

import aiohttp
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from semantic_chunkers import StatisticalChunker
from VectorSpace.Embedder import Embedder
import json
from dotenv import load_dotenv
import os
from authentication.models import UserText
from VectorSpace.Qdrant import VectorStore


from rag_backend import settings

from .serializers import QuizSerializer, SummarySerializer, TextSerializer



from typing import List

from pydantic import BaseModel, Field, field_validator


class Question(BaseModel):
    question: str = Field(description="The quiz question")
    options: List[str] = Field(description="List of multiple-choice options")
    correct_answers: List[str] = Field(description="List of correct answers")

    # @field_validator("options")
    # def check_options_length(cls, v):
    #     if len(v) != 4:
    #         raise ValueError("Each question must have exactly 4 options.")
    #     return v

    # @field_validator("correct_answers")
    # def check_correct_answers_length(cls, v):
    #     if len(v) != 1:
    #         raise ValueError("There must be exactly one correct answer.")
    #     return v


class Quiz(BaseModel):
    questions: List[Question] = Field(description="List of quiz questions")

class Summary(BaseModel):
    summary: str




load_dotenv()

vector_database = VectorStore()


headers = {os.getenv("API_KEY_NAME"): os.getenv("API_KEY")}
ip_server = os.getenv("IP_SERVER")
collection_name = os.getenv("COLLECTION")


async def generate_summary(data):
    async with aiohttp.ClientSession() as session:
        global headers, ip_server
        async with session.post(
            f"http://{ip_server}:8080/summary", json=data, headers=headers
        ) as response:
            data = await response.json()
            return data

text_splitter = StatisticalChunker(
    encoder=Embedder(),
    name="statistical_chunker",
    threshold_adjustment=0.01,
    dynamic_threshold=True,
    window_size=5,
    min_split_tokens=200,
    max_split_tokens=800,
    split_tokens_tolerance=10,
    plot_chunks=False,
    enable_statistics=False,
)


async def generate_summary(data):
    async with aiohttp.ClientSession() as session:
        global headers, ip_server
        async with session.post(
            f"http://{ip_server}:8080/summary", json=data, headers=headers
        ) as response:
            data = await response.json()
            return data


class SSEView(APIView):
    def get(self, request) -> StreamingHttpResponse:
        def event_stream():
            for i in range(10):
                sleep(1)
                question = {"question": "What is 2 + 2?",
                            "choices": ["3", "4", "5"]}
                yield f"data: {json.dumps(question)}\n\n"

        response = StreamingHttpResponse(
            event_stream(), content_type="text/event-stream"
        )
        return response


class SummaryView(APIView):
    def post(self, request, format=None) -> Response:
        print(request.user)
        serializer = SummarySerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data["text"]

            chunks = text_splitter(docs=[text])[0]
            batch_normilized = [" ".join(batch_chunk.splits)
                                for batch_chunk in chunks]
            data = {"text": batch_normilized}

            summary = data

            UserText.objects.create(
                user=request.user, text=text, summary=summary)

            vector_database.add(
                chunks=batch_normilized,
                idx=[uuid4() for _ in range(len(chunks))],
                metadata=[
                    {
                        "Payload": {
                            "user": "user",
                            "text": chunk,
                            "title": "title",
                            "topic": orig_chunk[0],
                        }
                    }
                    for chunk, orig_chunk in zip(batch_normilized, chunks)
                ],
                collection_name=collection_name,
            )

            return Response(summary)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetData(APIView):
    def get(self, request, format=None):
        user_texts = UserText.objects.filter(user=request.user)
        data = []
        for user_text in user_texts:
            data.append(
                {
                    "id": user_text.id,
                    "text": user_text.text,
                    "summary": user_text.summary,
                    "created_at": user_text.created_at,
                }
            )
        return Response(data, status=status.HTTP_200_OK)


class QuizView(APIView):
    def post(self, request, format=None):
        def event_stream(batch: list[str], topics: list[str] = None):
            global headers, ip_server
            batch_size = 2
            for i in range(0, len(batch), batch_size):
                data = {"text": batch[i: i + batch_size]}
                quiz_token = requests.post(
                    f"http://{ip_server}:8080/quiz/",
                    json=data,
                    headers=headers,
                )

                if topics and False == True:
                    vector_database.add(
                        chunks=batch[i: i + batch_size],
                        idx=[uuid4() for _ in range(len(batch_size))],
                        metadata=[
                            {
                                "Payload": {
                                    "user": "user",
                                    "text": chunk,
                                    "title": "title",
                                    "topic": topic,
                                }
                            }
                            for chunk, topic in zip(
                                batch[i: i + batch_size], topics[i: i + batch_size]
                            )
                        ],
                        collection_name=collection_name,
                    )
                sleep(3)
                waiting_for_gen = True
                while waiting_for_gen:
                    quiz = requests.get(
                        f'http://{ip_server}:8080/quiz/'
                        f'{quiz_token.json()["request_id"]}',
                        headers=headers,
                    )
                    if quiz.status_code == 404:
                        sleep(4)
                    else:
                        print(quiz, quiz.json())
                        waiting_for_gen = False
                        questions = quiz.json()["questions"]
                        print(questions)
                        for question in questions:
                            print(question)
                            yield f"data: {Quiz(questions=[question]).model_dump_json()}\n\n"

        serializer = TextSerializer(data=request.data)

        if serializer.is_valid():
            if False:
                data_batch = [
                    result.payload["text"]
                    for result in vector_database.search(
                        collection_name=collection_name,
                        query=text,
                        top=10,
                    )
                ]
                response = StreamingHttpResponse(
                    event_stream(batch=data_batch), content_type="text/event-stream"
                )
            else:
                text = serializer.validated_data["text"]

                chunks = text_splitter(docs=[text])[0]

                topics = [chunk.splits[0] for chunk in chunks]
                batch_normilized = [
                    " ".join(batch_chunk.splits) for batch_chunk in chunks
                ]

                response = StreamingHttpResponse(
                    event_stream(batch=batch_normilized, topics=topics),
                    content_type="text/event-stream",
                )
            response["Cache-Control"] = "no-cache"
            response["X-Accel-Buffering"] = "no"
            return response


def main(request) -> HttpResponse:
    return render(request, "main.html")
