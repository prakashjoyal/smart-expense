import json
from datetime import date
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import RegisterForm, TransactionForm, BudgetForm
from .models import Category, Transaction, Budget

DEFAULT_CATEGORIES = {
    "income": ["Salary", "Freelance", "Business", "Investment", "Other income"],
    "expense": ["Food", "Transport", "Shopping", "Bills", "Health", "Education", "Entertainment", "Rent", "Other expense"],
}

def seed_categories(user):
    for kind, names in DEFAULT_CATEGORIES.items():
        for name in names:
            Category.objects.get_or_create(user=user, name=name, kind=kind)

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
        )
        seed_categories(user)
        login(request, user)
        messages.success(request, "Your account is ready. Welcome!")
        return redirect("dashboard")
    return render(request, "registration/register.html", {"form": form})

@login_required
def dashboard(request):
    today = timezone.localdate()
    month_start = today.replace(day=1)
    qs = Transaction.objects.filter(user=request.user)
    month_qs = qs.filter(transaction_date__gte=month_start, transaction_date__lte=today)
    income = month_qs.filter(kind="income").aggregate(total=Sum("amount"))["total"] or Decimal("0")
    expense = month_qs.filter(kind="expense").aggregate(total=Sum("amount"))["total"] or Decimal("0")
    balance = (qs.filter(kind="income").aggregate(total=Sum("amount"))["total"] or Decimal("0")) - (qs.filter(kind="expense").aggregate(total=Sum("amount"))["total"] or Decimal("0"))

    category_rows = list(month_qs.filter(kind="expense").values("category__name").annotate(total=Sum("amount")).order_by("-total"))
    daily_rows = []
    for day in range(1, today.day + 1):
        d = today.replace(day=day)
        daily_rows.append({
            "label": d.strftime("%d"),
            "income": float(month_qs.filter(transaction_date=d, kind="income").aggregate(t=Sum("amount"))["t"] or 0),
            "expense": float(month_qs.filter(transaction_date=d, kind="expense").aggregate(t=Sum("amount"))["t"] or 0),
        })

    budgets = Budget.objects.filter(user=request.user, month__year=today.year, month__month=today.month).select_related("category")
    budget_cards = []
    for b in budgets:
        spent = month_qs.filter(kind="expense", category=b.category).aggregate(t=Sum("amount"))["t"] or Decimal("0")
        pct = min(100, int((spent / b.limit_amount) * 100)) if b.limit_amount else 0
        budget_cards.append({"budget": b, "spent": spent, "percent": pct, "over": spent > b.limit_amount})

    context = {
        "income": income, "expense": expense, "savings": income - expense, "balance": balance,
        "transactions": qs[:6], "category_labels": json.dumps([r["category__name"] for r in category_rows]),
        "category_values": json.dumps([float(r["total"]) for r in category_rows]),
        "daily_labels": json.dumps([r["label"] for r in daily_rows]),
        "daily_income": json.dumps([r["income"] for r in daily_rows]),
        "daily_expense": json.dumps([r["expense"] for r in daily_rows]),
        "budget_cards": budget_cards, "today": today,
    }
    return render(request, "expenses/dashboard.html", context)

@login_required
def transactions(request):
    qs = Transaction.objects.filter(user=request.user).select_related("category")
    kind = request.GET.get("kind", "")
    if kind in ("income", "expense"):
        qs = qs.filter(kind=kind)
    search = request.GET.get("q", "").strip()
    if search:
        qs = qs.filter(description__icontains=search)
    return render(request, "expenses/transactions.html", {"transactions": qs, "kind": kind, "search": search})

@login_required
def transaction_create(request):
    form = TransactionForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        messages.success(request, "Transaction added successfully.")
        return redirect("transactions")
    return render(request, "expenses/transaction_form.html", {"form": form, "heading": "Add transaction"})

@login_required
def transaction_update(request, pk):
    item = get_object_or_404(Transaction, pk=pk, user=request.user)
    form = TransactionForm(request.POST or None, instance=item, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Transaction updated.")
        return redirect("transactions")
    return render(request, "expenses/transaction_form.html", {"form": form, "heading": "Edit transaction"})

@login_required
def transaction_delete(request, pk):
    item = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Transaction deleted.")
    return redirect("transactions")

@login_required
def budgets(request):
    form = BudgetForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        messages.success(request, "Budget saved.")
        return redirect("budgets")
    today = timezone.localdate()
    budget_list = Budget.objects.filter(user=request.user).select_related("category")
    rows = []
    for b in budget_list:
        spent = Transaction.objects.filter(user=request.user, category=b.category, kind="expense",
            transaction_date__year=b.month.year, transaction_date__month=b.month.month
        ).aggregate(t=Sum("amount"))["t"] or Decimal("0")
        pct = min(100, int(spent / b.limit_amount * 100)) if b.limit_amount else 0
        rows.append({"budget": b, "spent": spent, "percent": pct, "over": spent > b.limit_amount})
    return render(request, "expenses/budgets.html", {"form": form, "budget_rows": rows, "today": today})

@login_required
def reports(request):
    qs = Transaction.objects.filter(user=request.user)
    year = int(request.GET.get("year", timezone.localdate().year))
    monthly = []
    for month in range(1, 13):
        inc = qs.filter(kind="income", transaction_date__year=year, transaction_date__month=month).aggregate(t=Sum("amount"))["t"] or 0
        exp = qs.filter(kind="expense", transaction_date__year=year, transaction_date__month=month).aggregate(t=Sum("amount"))["t"] or 0
        monthly.append({"label": date(year, month, 1).strftime("%b"), "income": float(inc), "expense": float(exp)})
    return render(request, "expenses/reports.html", {
        "year": year, "monthly_labels": json.dumps([x["label"] for x in monthly]),
        "monthly_income": json.dumps([x["income"] for x in monthly]),
        "monthly_expense": json.dumps([x["expense"] for x in monthly]),
    })
