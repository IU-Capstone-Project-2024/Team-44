from django.urls import path, include
from . import views
from .views import SignUpView, SignInView, SignOutView

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('api/signup/', SignUpView.as_view(), name='signup'),
    path('api/signin/', SignInView.as_view(), name='signin'),
    path('api/signout/', SignOutView.as_view(), name='signout'),

]
