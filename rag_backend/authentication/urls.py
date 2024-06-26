from django.urls import path, include
from . import views
from .views import SignUpView, SignInView, SignOutView, ConfirmEmailAPIView

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('api/signup/', SignUpView.as_view(), name='api-signup'),
    path('api/signin/', SignInView.as_view(), name='api-signin'),
    path('api/signout/', SignOutView.as_view(), name='api-signout'),
    path('api/email-verify', ConfirmEmailAPIView.as_view(), name='email-verify')
]
