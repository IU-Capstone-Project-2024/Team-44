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
from fastapi_ml.app.lang_graph.ValidationModels import Question
import json

import asyncio
import aiohttp

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
                question = {"question": "What is 2 + 2?",
                            "choices": ["3", "4", "5"]}
                yield f"data: {json.dumps(question)}\n\n"

        response = StreamingHttpResponse(
            event_stream(), content_type="text/event-stream"
        )
        return response


class SummaryView(APIView):
    def post(self, request, format=None):
        serializer = SummarySerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data["query"]

            chunks = text_splitter(docs=[query])[0]
            summaries = []
            for i in range(0, len(chunks), 2):
                print(len(chunks))
                batch_chunks = chunks[i: i + 2]
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
    def get(self, request, format=None):
        def event_stream():
            for i in range(0, 10, 2):
                sleep(20)
                quiz_serializer = QuizSerializer({
                    "questions": [
                        Question(
                            question="What is the process used by plants to convert light energy into chemical energy?",
                            options=["Respiration", "Photosynthesis",
                                     "Decomposition", "Evaporation"],
                            correct_answers=["Photosynthesis"],
                        )
                    ]
                })
                yield quiz_serializer.data

        # serializer = TextSerializer(data=request.data)
        # if serializer.is_valid():
        #     text = serializer.validated_data["text"]

        #     chunks = text_splitter(docs=[text])[0]

        response = StreamingHttpResponse(
            event_stream(), content_type="text/event-stream"
        )
        return response
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def main(request):
    return render(request, "main.html")
