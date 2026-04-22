from django.db import models
from django.contrib.auth.models import User


class BudgetEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    food = models.DecimalField(max_digits=10, decimal_places=2)
    transport = models.DecimalField(max_digits=10, decimal_places=2)
    utilities = models.DecimalField(max_digits=10, decimal_places=2)
    other = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"


class CostOfLivingEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    preferred_city = models.CharField(max_length=100, blank=True)
    best_city = models.CharField(max_length=100)
    best_shop = models.CharField(max_length=100)
    best_total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    best_remaining = models.DecimalField(max_digits=10, decimal_places=2)
    affordability_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.best_city} ({self.best_shop})"