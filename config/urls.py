from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from expenses import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("new-expense/", include("expenses.urls")),
]
