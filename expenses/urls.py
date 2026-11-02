from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("transactions/", views.transactions, name="transactions"),
    path("transactions/add/", views.transaction_create, name="transaction_create"),
    path("transactions/<int:pk>/edit/", views.transaction_update, name="transaction_update"),
    path("transactions/<int:pk>/delete/", views.transaction_delete, name="transaction_delete"),
    path("budgets/", views.budgets, name="budgets"),
    path("reports/", views.reports, name="reports"),
]
