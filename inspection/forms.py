from django import forms
from omni.forms import TimeRangeForm

class MoudleSearchForm(TimeRangeForm):
    CHOICES = (
        ('', 'ALL'),
        ('MISS', 'MISSING'),
        ('CH', 'CHANGED'),
        ('NEW', 'NEW'),
    )
    device_name = forms.CharField(label='Device', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GDFOS-IPMAN-BNG01-DS-HW', 'style':'width:230px'}))
    status = forms.ChoiceField(label='Status', choices=CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control', 'style':'width:70px'}))

class PortErrorSearchForm(TimeRangeForm):
    pass

class OneWaySearchForm(TimeRangeForm):
    pass