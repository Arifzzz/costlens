from django import forms
from django.contrib.auth.models import User


class BudgetForm(forms.Form):
    monthly_income = forms.DecimalField(
        label="Monthly Income (£)",
        min_value=0,
        decimal_places=2,
        max_digits=10,
        required=True,
        widget=forms.NumberInput(attrs={
            "class": "input-field",
            "placeholder": "e.g. 2000",
            "step": "0.01",
        }),
    )

    rent = forms.DecimalField(
        label="Rent (£)",
        min_value=0,
        decimal_places=2,
        max_digits=10,
        required=False,
        widget=forms.NumberInput(attrs={
            "class": "input-field",
            "placeholder": "e.g. 900",
            "step": "0.01",
        }),
    )

    food = forms.DecimalField(
        label="Food (£)",
        min_value=0,
        decimal_places=2,
        max_digits=10,
        required=False,
        widget=forms.NumberInput(attrs={
            "class": "input-field",
            "placeholder": "e.g. 250",
            "step": "0.01",
        }),
    )

    transport = forms.DecimalField(
        label="Transport (£)",
        min_value=0,
        decimal_places=2,
        max_digits=10,
        required=False,
        widget=forms.NumberInput(attrs={
            "class": "input-field",
            "placeholder": "e.g. 120",
            "step": "0.01",
        }),
    )

    utilities = forms.DecimalField(
        label="Utilities (£)",
        min_value=0,
        decimal_places=2,
        max_digits=10,
        required=False,
        widget=forms.NumberInput(attrs={
            "class": "input-field",
            "placeholder": "e.g. 150",
            "step": "0.01",
        }),
    )

    other = forms.DecimalField(
        label="Other Expenses (£)",
        min_value=0,
        decimal_places=2,
        max_digits=10,
        required=False,
        widget=forms.NumberInput(attrs={
            "class": "input-field",
            "placeholder": "e.g. 100",
            "step": "0.01",
        }),
    )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "input-field",
                "placeholder": "Enter username",
            }),
            "email": forms.EmailInput(attrs={
                "class": "input-field",
                "placeholder": "Enter email",
            }),
        }