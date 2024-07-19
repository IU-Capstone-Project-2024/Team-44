from django.urls import path, include
from . import views
from .views import SummaryView, QuizView, TimerView

from django.urls import path
from .views import SSEView


urlpatterns = [
    path('', views.main, name="main"),
    path('ml/', views.ml_view, name="ml"),
    path('summary/', SummaryView.as_view(), name='summary'),
    path('quiz/', QuizView.as_view(), name="quiz"),
    path('authentication/', include('authentication.urls')),
    path('timer/', TimerView.as_view(), name='timer'),
    path('quiz/sse/', SSEView.as_view(), name='quiz_sse'),

]
