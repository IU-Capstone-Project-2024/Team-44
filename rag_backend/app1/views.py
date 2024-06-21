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
        result = router.retrieve(query, 'similarity', {'k': 1})
        return JsonResponse({'result': result})


def main(request):
    return render(request, 'main.html')
