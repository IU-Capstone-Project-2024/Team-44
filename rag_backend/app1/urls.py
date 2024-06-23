from django.urls import path, include
from . import views
from .views import SummaryView, QuizView

urlpatterns = [
    path('', views.main, name="main"),
    path('ml/', views.ml_view, name="ml"),
    path('summary/', SummaryView.as_view(), name='summary'),
    path('quiz/', QuizView.as_view(), name="quiz"),
    path('authentication/', include('authentication.urls'))
]
