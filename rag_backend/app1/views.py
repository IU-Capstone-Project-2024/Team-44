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
from langchain.document_loaders import TextLoader


def document_to_dict(document):
    """
    Convert a Document object to a dictionary that can be serialized to JSON.
    """
    return {
        'page_content': document.page_content,
        'metadata': document.metadata,
    }


@csrf_exempt
def ml_view(request):
    if request.method == "POST":
        # if 'query' in request.POST:
        #     query = request.POST['query']
        # else:
        #     query = False
        query = request.POST.get('query')

        print(query)
        router = Router()
        # error : page_content method is not in tuple
        # doc = Document(page_content="This is the content of the document.", metadata={
        #                "source": "example.com"})
        # documents = [doc]
        loader = TextLoader("test_txt.txt")
        documents = loader.load()
        print(documents)
        verdict = router.add_docs(documents)
        result = router.retrieve(query)
        # result_dict = document_to_dict(result)
        print(result)
        # print(result_dict)
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
