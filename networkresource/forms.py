from django import forms

class IPsearchForm(forms.Form):
    ip_address = forms.GenericIPAddressField(label='IP', protocol='both', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1.1.1.1', 'style':'width:150px'}))
    device_name = forms.CharField(label='Device', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GDFOS-IPMAN-BNG01-DS-HW', 'style':'width:230px'}))
    description = forms.CharField(label='Description', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '...NanHai...', 'style':'width:300px'}))