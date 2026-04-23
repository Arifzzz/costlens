from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import BudgetEntry, CostOfLivingEntry
from .forms import UserUpdateForm


def landing(request):
    return render(request, "dashboard/index.html")


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()

    return render(request, "dashboard/signup.html", {"form": form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()

    return render(request, "dashboard/login.html", {"form": form})


@login_required
def dashboard(request):
    latest_entry = BudgetEntry.objects.filter(user=request.user).order_by("-created_at").first()
    recent_entries = BudgetEntry.objects.filter(user=request.user).order_by("-created_at")[:4]

    return render(request, "dashboard/home.html", {
        "latest_entry": latest_entry,
        "recent_entries": recent_entries,
    })


@login_required
def budget(request):
    result = None

    if request.method == "POST":
        monthly_income = Decimal(request.POST.get("monthly_income", "0"))
        rent = Decimal(request.POST.get("rent", "0"))
        food = Decimal(request.POST.get("food", "0"))
        transport = Decimal(request.POST.get("transport", "0"))
        utilities = Decimal(request.POST.get("utilities", "0"))
        other = Decimal(request.POST.get("other", "0"))

        total_expenses = rent + food + transport + utilities + other
        remaining_balance = monthly_income - total_expenses

        BudgetEntry.objects.create(
            user=request.user,
            monthly_income=monthly_income,
            rent=rent,
            food=food,
            transport=transport,
            utilities=utilities,
            other=other,
            total_expenses=total_expenses,
            remaining_balance=remaining_balance
        )

        result = {
            "monthly_income": monthly_income,
            "total_expenses": total_expenses,
            "remaining_balance": remaining_balance
        }

    return render(request, "dashboard/budget.html", {"result": result})


@login_required
def cost_of_living(request):
    result = None

    data = {
        "London": {
            "Tesco": {"rent": 1200, "food": 320, "transport": 150, "utilities": 120},
            "Aldi": {"rent": 1200, "food": 260, "transport": 150, "utilities": 120},
            "Sainsbury": {"rent": 1200, "food": 340, "transport": 150, "utilities": 120},
        },
        "Manchester": {
            "Tesco": {"rent": 800, "food": 280, "transport": 100, "utilities": 100},
            "Aldi": {"rent": 800, "food": 220, "transport": 100, "utilities": 100},
            "Sainsbury": {"rent": 800, "food": 300, "transport": 100, "utilities": 100},
        },
        "Birmingham": {
            "Tesco": {"rent": 750, "food": 260, "transport": 90, "utilities": 95},
            "Aldi": {"rent": 750, "food": 210, "transport": 90, "utilities": 95},
            "Sainsbury": {"rent": 750, "food": 280, "transport": 90, "utilities": 95},
        },
    }

    if request.method == "POST":
        monthly_salary = Decimal(request.POST.get("salary", "0"))
        preferred_city = request.POST.get("preferred_city", "")

        comparisons = []

        for city, shops in data.items():
            for shop, costs in shops.items():
                total_cost = Decimal(str(sum(costs.values())))
                remaining = monthly_salary - total_cost

                if monthly_salary > 0:
                    score = int(max(0, min(100, (remaining / monthly_salary) * 100)))
                else:
                    score = 0

                if score >= 40:
                    status = "Comfortable"
                elif score >= 20:
                    status = "Manageable"
                elif score >= 0:
                    status = "Tight"
                else:
                    status = "Unaffordable"

                comparisons.append({
                    "city": city,
                    "shop": shop,
                    "rent": costs["rent"],
                    "food": costs["food"],
                    "transport": costs["transport"],
                    "utilities": costs["utilities"],
                    "total": total_cost,
                    "remaining": remaining,
                    "score": score,
                    "status": status,
                    "preferred": city == preferred_city,
                })

        best_option = min(comparisons, key=lambda x: x["total"])

        CostOfLivingEntry.objects.create(
            user=request.user,
            salary=monthly_salary,
            preferred_city=preferred_city,
            best_city=best_option["city"],
            best_shop=best_option["shop"],
            best_total_cost=best_option["total"],
            best_remaining=best_option["remaining"],
            affordability_score=best_option["score"],
        )

        result = {
            "monthly_salary": monthly_salary,
            "preferred_city": preferred_city,
            "comparisons": comparisons,
            "best": best_option,
        }

    return render(request, "dashboard/costofliving.html", {"result": result})


@login_required
def profile(request):
    message = ""

    if request.method == "POST":
        if "update_details" in request.POST:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            password_form = PasswordChangeForm(request.user)

            if user_form.is_valid():
                user_form.save()
                message = "Account details updated successfully."
            else:
                password_form = PasswordChangeForm(request.user)

        elif "change_password" in request.POST:
            user_form = UserUpdateForm(instance=request.user)
            password_form = PasswordChangeForm(request.user, request.POST)

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                message = "Password updated successfully."
        else:
            user_form = UserUpdateForm(instance=request.user)
            password_form = PasswordChangeForm(request.user)
    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, "dashboard/profile.html", {
        "user_form": user_form,
        "password_form": password_form,
        "message": message,
    })


@login_required
def history(request):
    budget_history = BudgetEntry.objects.filter(user=request.user).order_by("-created_at")
    cost_history = CostOfLivingEntry.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "dashboard/history.html", {
        "budget_history": budget_history,
        "cost_history": cost_history,
    })


def user_logout(request):
    logout(request)
    return redirect("landing")