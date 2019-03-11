from django import forms

class IPsearchForm(forms.Form):
    ip_address = forms.GenericIPAddressField(label='IP', protocol='both', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1.1.1.1', 'style':'width:150px'}))
    device_name = forms.CharField(label='Device', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GDFOS-IPMAN-BNG01-DS-HW', 'style':'width:230px'}))
    description = forms.CharField(label='Description', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '...NanHai...', 'style':'width:300px'}))

    def clean(self):
        cleaned_data = super().clean()
        ip_address = cleaned_data.get('ip_address')
        device_name = cleaned_data.get('device_name')
        description = cleaned_data.get('description')
        if ip_address == device_name == description == '':
            raise forms.ValidationError('Please specify at least one claus.')
        return self.cleaned_data

class PortSearchForm(forms.Form):
    device_name = forms.CharField(label='Device', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GDFOS-IPMAN-BNG01-DS-HW'}))
    slot = forms.IntegerField(label='Slot', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 1}))
    port = forms.CharField(label='Port', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1/1/1'}))
    port_description = forms.CharField(label='Description', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '..NanHai...'}))

    def clean(self):
        cleaned_data = super().clean()
        device_name = cleaned_data.get('device_name')
        slot = cleaned_data.get('slot') # slot是数字类型，如果没有，则返回None，非''
        port = cleaned_data.get('port')
        port_description = cleaned_data.get('port_description')
        if slot is None and port == port_description == '':
            raise forms.ValidationError('Please specify Device_name and one of (Slot, Port, Description)')
            
        return self.cleaned_data

