from django import forms
from .models import Transaction, Budget, Category

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Choose a username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email address"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "At least 8 characters"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Repeat password"}))

    def clean(self):
        data = super().clean()
        if data.get("password") and data.get("confirm_password") and data["password"] != data["confirm_password"]:
            self.add_error("confirm_password", "Passwords do not match.")
        return data

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["kind", "category", "amount", "description", "transaction_date"]
        widgets = {
            "kind": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.01"}),
            "description": forms.TextInput(attrs={"class": "form-control", "placeholder": "What was this transaction for?"}),
            "transaction_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["category"].queryset = Category.objects.filter(user=user) if user else Category.objects.none()

    def clean(self):
        data = super().clean()
        category, kind = data.get("category"), data.get("kind")
        if category and kind and category.kind != kind:
            self.add_error("category", "Choose a category matching the transaction type.")
        return data

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["category", "month", "limit_amount"]
        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),
            "month": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "limit_amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.01"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(user=user, kind="expense") if user else Category.objects.none()
