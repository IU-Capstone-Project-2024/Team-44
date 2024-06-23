from django.urls import path, include
from . import views
from .views import QueryView

urlpatterns = [
    path('', views.main, name="main"),
    path('ml/', views.ml_view, name="ml"),
    path('ml-api/', QueryView.as_view(), name='mp-api'),
    path('authentication/', include('authentication.urls'))
]
