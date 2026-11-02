from django.conf import settings
from django.db import models
from django.utils import timezone

class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="expense_categories")
    name = models.CharField(max_length=60)
    kind = models.CharField(max_length=10, choices=[("income", "Income"), ("expense", "Expense")])

    class Meta:
        ordering = ["name"]
        unique_together = ("user", "name", "kind")

    def __str__(self):
        return f"{self.name} ({self.kind})"

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="transactions")
    kind = models.CharField(max_length=10, choices=[("income", "Income"), ("expense", "Expense")])
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=240)
    transaction_date = models.DateField(default=timezone.localdate)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-transaction_date", "-created_at"]

    def __str__(self):
        return f"{self.kind}: {self.amount} - {self.description}"

class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="budgets")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, limit_choices_to={"kind": "expense"})
    month = models.DateField(help_text="Choose any date in the budget month")
    limit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-month"]
        unique_together = ("user", "category", "month")

    def __str__(self):
        return f"{self.category.name} - {self.month:%B %Y}"
