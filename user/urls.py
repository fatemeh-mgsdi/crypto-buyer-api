from django.urls import path

from user.views import UserRegisterView, LoginRegisterView


urlpatterns = [
    path("user/register/", UserRegisterView.as_view(), name="register"),
    path("user/login/", LoginRegisterView.as_view(), name="login"),

]