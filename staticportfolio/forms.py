from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    fullname = forms.CharField(
        label="Full name",
        max_length=160,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "Full name",
                "data-form-input": "",
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-input",
                "placeholder": "Email Address",
                "data-form-input": "",
            }
        )
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-input",
                "placeholder": "Your Message",
                "data-form-input": "",
            }
        )
    )

    class Meta:
        model = ContactMessage
        fields = ("email", "message")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.full_name = self.cleaned_data["fullname"]
        if commit:
            instance.save()
        return instance
