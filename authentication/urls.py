from django.urls import path
from .views import UserRegisterView, LoginView,LogoutView,CustomerDetails
urlpatterns = [
    path("register/", UserRegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("details/", CustomerDetails.as_view())
]