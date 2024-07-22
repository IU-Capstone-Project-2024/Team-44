from django.http import HttpResponse, StreamingHttpResponse
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

from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import TextSplitter
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from semantic_chunkers import StatisticalChunker
from VectorSpace.Embedder import Embedder
import json
from dotenv import load_dotenv
import os
from authentication.models import UserText


import asyncio
import aiohttp

headers = {os.getenv("API_KEY_NAME"): os.getenv("API_KEY")}
ip_server = os.getenv("IP_SERVER")

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
                question = {"question": "What is 2 + 2?", "choices": ["3", "4", "5"]}
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
            data = {"text": [" ".join(batch_chunk.splits) for batch_chunk in chunks]}

            summary = data

            UserText.objects.create(user=request.user, text=text, summary=summary)

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
        def event_stream(chunks: list[str]):
            global headers, ip_server
            for i in range(0, len(chunks), 2):
                batch_chunks = chunks[i : i + 2]
                data = {
                    "text": [
                        " ".join(batch_chunk.splits) for batch_chunk in batch_chunks
                    ]
                }
                quiz_token = requests.post(
                    f"http://{ip_server}:8080/quiz/",
                    json=data,
                    headers=headers,
                )
                sleep(4)
                waiting_for_gen = True
                while waiting_for_gen:
                    quiz = requests.get(
                        f'http://{ip_server}:8080/quiz/{quiz_token.json()
                                                        ["request_id"]}',
                        headers=headers,
                    )
                    if quiz.status_code == 404:
                        sleep(4)
                    else:
                        print(quiz, quiz.json())
                        waiting_for_gen = False
                        yield f"data: {quiz.json()}\n\n"

        serializer = TextSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data["text"]

            chunks = text_splitter(docs=[text])[0]

            response = StreamingHttpResponse(
                event_stream(chunks), content_type="text/event-stream"
            )
            return response


def main(request) -> HttpResponse:
    return render(request, "main.html")
