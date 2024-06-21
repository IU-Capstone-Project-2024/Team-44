from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('ml/', views.ml_view, name="ml"),
    path('authentication/', include('authentication.urls'))
]
