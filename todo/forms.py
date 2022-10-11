
from django import forms

def_errors = {
    "required": "این فیلد نمیتواند خالی باشد"
}
class TodoAddForm(forms.Form):
    title = forms.CharField(max_length=200,error_messages=def_errors)
    time_to_do = forms.DateTimeField(
                input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'data-target': '#datetimepicker1',
            "id":"time_to_do",
            "disable": True
        }),required=False
    )

DATE_CHOICES =(
    ("0", "All"),
    ("1", "ToDay"),
    ("2", "Yesterday"),
    ("3", "1 weekago"),
)
DONE_CHOICES =(
    ("0", "All"),
    ("1", "Done"),
    ("2", "UnDone"),
)

class TodoSearchForm(forms.Form):
    search = forms.CharField(label="",required=False)
    date = forms.ChoiceField(choices=DATE_CHOICES,widget=forms.Select(attrs={'onchange': 'submit();'}))
    done_status = forms.ChoiceField(choices=DONE_CHOICES,widget=forms.Select(attrs={'onchange': 'submit();'}))
    
class TodoEditForm(forms.Form):
    title = forms.CharField(max_length=200)


#  XD soft Datetime picker
class XDateTimePickerForm(forms.Form):
    date = forms.DateTimeField(
                input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        }),label="Time To Do"
    )
