from django import forms
import datetime

class MoudleSearchForm(forms.Form):
    CHOICES = (
        ('', 'ALL'),
        ('MISS', 'MISSING'),
        ('CH', 'CHANGED'),
        ('NEW', 'NEW'),
    )
    device_name = forms.CharField(label='Device', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GDFOS-IPMAN-BNG01-DS-HW', 'style':'width:230px'}))
    status = forms.ChoiceField(label='Status', choices=CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control', 'style':'width:70px'}))
    time_begin = forms.DateTimeField(label='From', widget=forms.TextInput(attrs={'class': 'form-control form_datetime', 'placeholder': '2018-01-01 00:00:00', 'style':'width:160px', 'readonly': True}))
    time_end = forms.DateTimeField(label='to', widget=forms.TextInput(attrs={'class': 'form-control form_datetime', 'placeholder': '2018-01-11 23:59:59', 'style':'width:160px', 'readonly': True}))

    def clean(self):
        # super().clean()
        # time_begin = self.cleaned_data['time_begin']
        # time_end = self.cleaned_data['time_end']
        cleaned_data = super().clean()  # 保证先继承原有的字段验证，进行初步验证
        time_begin = cleaned_data.get('time_begin')
        time_end = cleaned_data.get('time_end')
        if type(time_begin) is str and type(time_end) is str:
            try:
                time_begin = datetime.datetime.strptime(time_begin, '%Y-%m-%d+%H:%M:%S')
                self.cleaned_data['time_begin'] = time_begin
                time_end = datetime.datetime.strptime(time_end, '%Y-%m-%d+%H:%M:%S')
                self.cleaned_data['time_end'] = time_end
            except:
                raise forms.ValidationError('Time Format Error. Input should like "2018-01-01 00:00:00"')
        if type(time_begin) is datetime.datetime and type(time_end) is datetime.datetime:
            if time_begin >= time_end:
                raise forms.ValidationError('Begin Time must earlier than End Time.')

        return self.cleaned_data
