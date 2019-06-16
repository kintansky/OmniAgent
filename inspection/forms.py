from django import forms
from omni.forms import TimeRangeForm

class MoudleSearchForm(TimeRangeForm):
    CHOICES = (
        ('', 'ALL'),
        ('MISS', 'MISSING'),
        ('CH', 'CHANGED'),
        ('NEW', 'NEW'),
    )
    device_name = forms.CharField(label='设备', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GDFOS-IPMAN-BNG01-DS-HW', 'style':'width:230px'}))
    status = forms.ChoiceField(label='状态', choices=CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control', 'style':'width:70px'}))


class PortErrorSearchForm(TimeRangeForm):
    pass


class PortErrorOperationForm(forms.Form):
    CHOICES = (
        ('power', '光功率问题'),
        ('moudle', '光模块故障'),
        ('fiber', '尾纤问题'),
        ('wdm', '波分故障'),
        ('other', '其他故障'),
    )
    problem_type = forms.ChoiceField(label='* 问题类型', choices=CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    problem_detail = forms.CharField(label='* 问题详情', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '...'}))

    def clean_problem_detail(self):
        problem_type = self.cleaned_data['problem_type']
        problem_detail = self.cleaned_data['problem_detail'].strip()
        if problem_type == 'other' and problem_detail == '':
            raise forms.ValidationError('问题类型为其他时，请填写详情')
        else:
            return problem_detail


class OneWaySearchForm(TimeRangeForm):
    pass


class GroupClientSearchForm(forms.Form):
    client_name = forms.CharField(label='客户名', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '****'}))
    product_id = forms.IntegerField(label='产品编码', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '20401****'}))

    def clean_client_name(self):
        return self.cleaned_data['client_name'].strip()


class NatPoolSearchForm(TimeRangeForm):
    device_name = forms.CharField(label='设备', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GDFOS-IPMAN-BNG01-DS-HW', 'style':'width:230px'}))

    def clean_device_name(self):
        return self.cleaned_data['device_name'].strip()