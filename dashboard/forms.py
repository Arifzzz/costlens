from django import forms  # Django form tools used to create input forms
from django.contrib.auth.models import User  # Built-in user model for accounts


class BudgetForm(forms.Form):  # Form used for budget calculator inputs
    monthly_income = forms.DecimalField(
        label="Monthly Income (£)",  # Label shown on page
        min_value=0,  # Prevents negative values
        decimal_places=2,  # Allows pence values
        max_digits=10,  # Max number length
        required=True,  # Must be entered
        widget=forms.NumberInput(attrs={
            "class": "input-field",  # CSS styling class
            "placeholder": "e.g. 2000",  # Example shown in box
            "step": "0.01",  # Allows decimals
        }),
    )

    rent = forms.DecimalField(
        label="Rent (£)",  # Rent input
        min_value=0,
        decimal_places=2,
        max_digits=10,
        required=False,  # Optional field
        widget=forms.NumberInput(attrs={
            "class": "input-field",
            "placeholder": "e.g. 900",
            "step": "0.01",
        }),
    )

    food = forms.DecimalField(
        label="Food (£)",  # Food spending input
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
        label="Transport (£)",  # Travel cost input
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
        label="Utilities (£)",  # Bills input
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
        label="Other Expenses (£)",  # Extra spending input
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


class UserUpdateForm(forms.ModelForm):  # Form used to update profile details
    class Meta:  # Settings for this model form
        model = User  # Uses Django built-in User table
        fields = ["username", "email"]  # Only editable fields shown
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "input-field",  # CSS styling
                "placeholder": "Enter username",  # Input hint
            }),
            "email": forms.EmailInput(attrs={
                "class": "input-field",  # CSS styling
                "placeholder": "Enter email",  # Input hint
            }),
        }