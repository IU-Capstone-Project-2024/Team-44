from django.urls import path, include
from . import views
from .views import SummaryView, QuizView, GetData

from django.urls import path
from .views import SSEView


urlpatterns = [
    path('', views.main, name="main"),
    path('summary/', SummaryView.as_view(), name='summary'),
    path('quiz/', QuizView.as_view(), name="quiz"),
    path('authentication/', include('authentication.urls')),
    path('quiz/sse/', SSEView.as_view(), name='quiz_sse'),
    path('get-data/', GetData.as_view(), name='get-data')
]
