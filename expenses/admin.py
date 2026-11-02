from django.contrib import admin
from .models import Category, Transaction, Budget

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "kind", "user")
    list_filter = ("kind",)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("description", "user", "kind", "amount", "category", "transaction_date")
    list_filter = ("kind", "transaction_date")
    search_fields = ("description", "user__username")

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "month", "limit_amount")
