
from django import forms


class TodoAddForm(forms.Form):
    title = forms.CharField(max_length=200)


class TodoSearchForm(forms.Form):
    search = forms.CharField()

DATE_CHOICES =(
    ("0", "All"),
    ("1", "One"),
    ("2", "Two"),
    ("3", "Three"),
)

class TodoDateFilterForm(forms.Form):
    date = forms.ChoiceField(choices=DATE_CHOICES,widget=forms.Select(attrs={'onchange': 'submit();'}))