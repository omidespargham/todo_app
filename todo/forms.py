
from django import forms


class TodoAddForm(forms.Form):
    title = forms.CharField(max_length=200)

DATE_CHOICES =(
    ("0", "All"),
    ("1", "ToDay"),
    ("2", "Yesterday"),
    ("3", "1 weekago"),
)

class TodoSearchForm(forms.Form):
    search = forms.CharField(label="",required=False)
    date = forms.ChoiceField(choices=DATE_CHOICES,widget=forms.Select(attrs={'onchange': 'submit();'}))


# class TodoDateFilterForm(forms.Form):
#     date = forms.ChoiceField(choices=DATE_CHOICES,widget=forms.Select(attrs={'onchange': 'submit();'}))