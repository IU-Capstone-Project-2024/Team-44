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
        #error : page_content method is not in tuple 
        doc = Document(page_content="This is the content of the document.", metadata={"source": "example.com"}) 
        documents = [doc]
        verdict = router.add_docs(documents)
        result = router.retrieve(query, 'similarity', {'k': 1})
        results = [
            {'result': result}, 
            {'document_isAdded': verdict}, 
        ]
        return JsonResponse(results)

@csrf_exempt
def add_docs(request):
    router = Router() 
    doc = Document(page_content="This is the content of the document.", metadata={"source": "example.com"}) 
    documents = [doc]
    verdict = router.add_docs(documents)
    result = [{'result': verdict}]
    return JsonResponse(result) 

def main(request):
    return render(request, 'main.html')


