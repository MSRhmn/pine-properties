from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your full name"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "your@email.com"}
        )
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Phone (optional)"}
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 4, "placeholder": "Your message"}
        )
    )
