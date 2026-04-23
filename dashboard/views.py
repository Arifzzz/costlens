from decimal import Decimal  # Used for accurate money calculations
from django.shortcuts import render, redirect  # Loads pages and redirects users
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm  # Built-in auth forms
from django.contrib.auth import login, logout, update_session_auth_hash  # Login/logout/session tools
from django.contrib.auth.decorators import login_required  # Protects pages from guests
from .models import BudgetEntry, CostOfLivingEntry  # Import database models
from .forms import UserUpdateForm  # Custom form for updating account details


def landing(request):  # Public homepage view
    return render(request, "dashboard/index.html")  # Render landing page template


def signup(request):  # User registration view
    if request.user.is_authenticated:  # If already logged in
        return redirect("dashboard")  # Send user to dashboard

    if request.method == "POST":  # If form submitted
        form = UserCreationForm(request.POST)  # Create signup form with user data
        if form.is_valid():  # Check if form passes validation
            user = form.save()  # Save new user account
            login(request, user)  # Automatically log user in
            return redirect("dashboard")  # Redirect after signup
    else:
        form = UserCreationForm()  # Empty signup form on first load

    return render(request, "dashboard/signup.html", {"form": form})  # Show signup page


def user_login(request):  # Login view
    if request.user.is_authenticated:  # If already logged in
        return redirect("dashboard")  # Skip login page

    if request.method == "POST":  # If login form submitted
        form = AuthenticationForm(request, data=request.POST)  # Create auth form
        if form.is_valid():  # Validate username/password
            user = form.get_user()  # Get logged in user
            login(request, user)  # Start user session
            return redirect("dashboard")  # Send to dashboard
    else:
        form = AuthenticationForm()  # Empty login form

    return render(request, "dashboard/login.html", {"form": form})  # Show login page


@login_required  # Requires user login
def dashboard(request):  # Main dashboard page
    latest_entry = BudgetEntry.objects.filter(user=request.user).order_by("-created_at").first()  # Most recent budget entry
    recent_entries = BudgetEntry.objects.filter(user=request.user).order_by("-created_at")[:4]  # Last 4 entries

    return render(request, "dashboard/home.html", {
        "latest_entry": latest_entry,
        "recent_entries": recent_entries,
    })  # Load dashboard page with data


@login_required  # Requires login
def budget(request):  # Budget calculator page
    result = None  # Empty result until calculation

    if request.method == "POST":  # If form submitted
        monthly_income = Decimal(request.POST.get("monthly_income", "0"))  # Get income
        rent = Decimal(request.POST.get("rent", "0"))  # Get rent
        food = Decimal(request.POST.get("food", "0"))  # Get food cost
        transport = Decimal(request.POST.get("transport", "0"))  # Get transport cost
        utilities = Decimal(request.POST.get("utilities", "0"))  # Get utilities cost
        other = Decimal(request.POST.get("other", "0"))  # Get other spending

        total_expenses = rent + food + transport + utilities + other  # Add all expenses
        remaining_balance = monthly_income - total_expenses  # Remaining money after bills

        BudgetEntry.objects.create(  # Save budget history
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

        result = {  # Results shown to user
            "monthly_income": monthly_income,
            "total_expenses": total_expenses,
            "remaining_balance": remaining_balance
        }

    return render(request, "dashboard/budget.html", {"result": result})  # Show budget page


@login_required  # Requires login
def cost_of_living(request):  # City affordability comparison page
    result = None  # No results at first

    data = {  # Static project dataset
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

    if request.method == "POST":  # If comparison form submitted
        monthly_salary = Decimal(request.POST.get("salary", "0"))  # User salary
        preferred_city = request.POST.get("preferred_city", "")  # User chosen city

        comparisons = []  # Stores all results

        for city, shops in data.items():  # Loop through each city
            for shop, costs in shops.items():  # Loop through each shop
                total_cost = Decimal(str(sum(costs.values())))  # Add living costs
                remaining = monthly_salary - total_cost  # Salary left after expenses

                if monthly_salary > 0:
                    score = int(max(0, min(100, (remaining / monthly_salary) * 100)))  # Affordability score
                else:
                    score = 0  # Prevent divide by zero

                if score >= 40:
                    status = "Comfortable"
                elif score >= 20:
                    status = "Manageable"
                elif score >= 0:
                    status = "Tight"
                else:
                    status = "Unaffordable"

                comparisons.append({  # Save comparison result
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

        best_option = min(comparisons, key=lambda x: x["total"])  # Cheapest option found

        CostOfLivingEntry.objects.create(  # Save comparison history
            user=request.user,
            salary=monthly_salary,
            preferred_city=preferred_city,
            best_city=best_option["city"],
            best_shop=best_option["shop"],
            best_total_cost=best_option["total"],
            best_remaining=best_option["remaining"],
            affordability_score=best_option["score"],
        )

        result = {  # Send results to page
            "monthly_salary": monthly_salary,
            "preferred_city": preferred_city,
            "comparisons": comparisons,
            "best": best_option,
        }

    return render(request, "dashboard/costofliving.html", {"result": result})  # Show comparison page


@login_required  # Requires login
def profile(request):  # User profile page
    message = ""  # Success message placeholder

    if request.method == "POST":
        if "update_details" in request.POST:  # If updating username/email
            user_form = UserUpdateForm(request.POST, instance=request.user)
            password_form = PasswordChangeForm(request.user)

            if user_form.is_valid():
                user_form.save()  # Save account changes
                message = "Account details updated successfully."
            else:
                password_form = PasswordChangeForm(request.user)

        elif "change_password" in request.POST:  # If changing password
            user_form = UserUpdateForm(instance=request.user)
            password_form = PasswordChangeForm(request.user, request.POST)

            if password_form.is_valid():
                user = password_form.save()  # Save new password
                update_session_auth_hash(request, user)  # Keep user logged in
                message = "Password updated successfully."
        else:
            user_form = UserUpdateForm(instance=request.user)
            password_form = PasswordChangeForm(request.user)
    else:
        user_form = UserUpdateForm(instance=request.user)  # Load default forms
        password_form = PasswordChangeForm(request.user)

    return render(request, "dashboard/profile.html", {
        "user_form": user_form,
        "password_form": password_form,
        "message": message,
    })  # Show profile page


@login_required  # Requires login
def history(request):  # View saved history page
    budget_history = BudgetEntry.objects.filter(user=request.user).order_by("-created_at")  # Budget history
    cost_history = CostOfLivingEntry.objects.filter(user=request.user).order_by("-created_at")  # Cost comparison history

    return render(request, "dashboard/history.html", {
        "budget_history": budget_history,
        "cost_history": cost_history,
    })  # Show history page


def user_logout(request):  # Logout view
    logout(request)  # End user session
    return redirect("landing")  # Return to landing page