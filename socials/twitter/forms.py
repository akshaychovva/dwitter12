from .models import Dweet
from django import forms

class DweetForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                    "placeholder": "Dweet something...",
                    "class": "textarea is-success is-medium",
                }
            ),
            label="",
    )
    
    class Meta:
        model = Dweet
        exclude = ("user", "num_of_edit")
