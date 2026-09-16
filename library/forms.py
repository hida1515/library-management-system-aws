from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Book, Member, Borrowing


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'isbn', 'category', 'publisher',
            'publication_year', 'quantity', 'available_quantity'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 978-3-16-148410-0'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Computer Science, Fiction'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter publisher name'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2024'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'available_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        available_quantity = cleaned_data.get('available_quantity')

        if quantity is not None and available_quantity is not None:
            if available_quantity > quantity:
                raise forms.ValidationError("Available quantity cannot exceed total quantity.")
        return cleaned_data


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'phone', 'membership_id', 'address', 'joined_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@domain.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 555-0199'}),
            'membership_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. LIB-2026-001'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Residential Address'}),
            'joined_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class BorrowingForm(forms.ModelForm):
    class Meta:
        model = Borrowing
        fields = ['book', 'member', 'due_date']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-select'}),
            'member': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show only books that have available_quantity > 0
        self.fields['book'].queryset = Book.objects.filter(available_quantity__gt=0)
        # Default due date to 14 days from today
        if not self.initial.get('due_date'):
            self.initial['due_date'] = (timezone.now() + timedelta(days=14)).strftime('%Y-%m-%d')
