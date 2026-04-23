from django.db import models  # Lets me create database tables using Django models
from django.contrib.auth.models import User  # Uses Django built-in user system for accounts


class BudgetEntry(models.Model):  # Table used to store budget calculator history
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links each entry to the logged in user
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)  # User monthly income
    rent = models.DecimalField(max_digits=10, decimal_places=2)  # Rent cost
    food = models.DecimalField(max_digits=10, decimal_places=2)  # Food spending
    transport = models.DecimalField(max_digits=10, decimal_places=2)  # Transport spending
    utilities = models.DecimalField(max_digits=10, decimal_places=2)  # Bills like gas/electric/water
    other = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Any extra spending
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2)  # Total of all expenses
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2)  # Money left after spending
    created_at = models.DateTimeField(auto_now_add=True)  # Saves date/time automatically

    def __str__(self):  # What shows in admin panel / database view
        return f"{self.user.username} - {self.created_at}"  # Username and date of entry


class CostOfLivingEntry(models.Model):  # Table used to save city comparison history
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links result to logged in user
    salary = models.DecimalField(max_digits=10, decimal_places=2)  # User salary entered
    preferred_city = models.CharField(max_length=100, blank=True)  # City user selected
    best_city = models.CharField(max_length=100)                           # Cheapest / best city found
    best_shop = models.CharField(max_length=100)                          # Best shop option found
    best_total_cost = models.DecimalField(max_digits=10, decimal_places=2)             # Total monthly cost
    best_remaining = models.DecimalField(max_digits=10, decimal_places=2)               # Money left after costs
    affordability_score = models.IntegerField()                                        # Score out of 100 for affordability
    created_at = models.DateTimeField(auto_now_add=True)                                # Auto saves date/time

    def __str__(self):                                                                # Display name for each saved result
        return f"{self.user.username} - {self.best_city} ({self.best_shop})"                                              # Username + best result