from django import forms
from .models import DeviceManufactor, Device


class AddDeviceForm(forms.Form):
    device_name = forms.CharField(label='Device Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'GDFOS-IPMAN-BNG01-DS-HW'}))
    device_ip = forms.GenericIPAddressField(label='IP Address', protocol='both', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '1.1.1.1'}))
    device_manufactor = forms.CharField(label='Manufactor', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'huawei'}))
    device_network = forms.CharField(label='Network', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'IPMAN'}))
    login_user = forms.CharField(label='User', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'admin'}))
    login_port = forms.IntegerField(label='Port', widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 22}))
    login_password = forms.CharField(label='Password', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'password'}))

    def clean(self):    # is_valid自动调用
        dv = self.cleaned_data['device_name']
        if Device.objects.filter(device_name=dv):
            # raise forms.ValidationError('重复的设备名')
            self.add_error('device_name', '重复的设备名')
        ip = self.cleaned_data['device_ip']
        if Device.objects.filter(device_ip=ip):
            self.add_error('device_ip', '重复的IP')
        dm = self.cleaned_data['device_manufactor']
        if DeviceManufactor.objects.filter(manufactor_name=dm):
            pass
        else:
            self.add_error('device_manufactor', '暂不支持的厂家')

        return self.cleaned_data
