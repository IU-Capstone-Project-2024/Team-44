from .serializers import SummarySerializer, QuizSerializer, TextSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import JsonResponse
from lang_graph.router import Router
from django.views.decorators.csrf import csrf_exempt
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
from lang_graph.agents.ValidationModels import Question
router = Router()


class SummaryView(APIView):
    def post(self, request, format=None):
        serializer = SummarySerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data['query']

            text_splitter = RecursiveCharacterTextSplitter()

            texts = text_splitter.create_documents([query])

            # print(document)
            # print(type(document))
            # document_loader = TextSplitter()
            # document = document_loader.create_documents([query])
            # loader = TextLoader("test_txt.txt")
            # documents = loader.load()
            summary = router.generate_summary(texts)
            # router.add_docs(documents)
            # result = router.retrieve(query)
            response_data = {
                'summary': summary,
                # 'retrieved_results': [doc.page_content for doc in result]
            }
            return Response(response_data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizView(APIView):
    def post(self, request, format=None):
        serializer = TextSerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data['text']

            text_splitter = RecursiveCharacterTextSplitter()

            text = text_splitter.create_documents([query])

            # Working with real model
            quiz_json = router.generate_quiz(text)
            quiz_serializer = QuizSerializer(quiz_json)

            # For testing:
            # quiz_serializer = QuizSerializer({
            #     "questions": [
            #         Question(
            #             question="What is the process used by plants to convert light energy into chemical energy?",
            #             options=["Respiration", "Photosynthesis",
            #                      "Decomposition", "Evaporation"],
            #             correct_answers=["Photosynthesis"],
            #         )
            #     ]
            # })
            # print(quiz_serializer.data)
            # print(quiz_serializer)
            return Response(quiz_serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def ml_view(request):
    if request.method == "POST":
        query = request.POST.get('query')

        print(query)
        loader = TextLoader("test_txt.txt")
        documents = loader.load()
        print(documents)
        summary = router.generate_summary(documents)
        verdict = router.add_docs(documents)
        result = router.retrieve(query)
        print(result)
        print('summary:', summary)
        results = {
            'result-1': result[0].page_content,
            'result-2': result[1].page_content,
            'result-3': result[2].page_content,
            'result-4': result[3].page_content,
            'document_isAdded': verdict,
        }
        return JsonResponse(results)

# @csrf_exempt
# def add_docs(request):
#     router = Router()
#     doc = Document(page_content="This is the content of the document.", metadata={"source": "example.com"})
#     documents = [doc]
#     verdict = router.add_docs(documents)
#     result = [{'result': verdict}]
#     return JsonResponse(result)


def main(request):
    return render(request, 'main.html')
