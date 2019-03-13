from django import forms
import re

class IPsearchForm(forms.Form):
    ip_address = forms.GenericIPAddressField(label='IP', protocol='both', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1.1.1.1', 'style':'width:150px'}))
    device_name = forms.CharField(label='Device', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GDFOS-IPMAN-BNG01-DS-HW', 'style':'width:230px'}))
    description = forms.CharField(label='Description', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '...NanHai...', 'style':'width:300px'}))

    def clean(self):
        cleaned_data = super().clean()
        ip_address = cleaned_data.get('ip_address')
        device_name = cleaned_data.get('device_name')
        description = cleaned_data.get('description')
        # if ip_address == device_name == description == '':
        #     raise forms.ValidationError('Please specify at least one claus.')
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

# IP 分配操作相关
class IpAllocateForm(forms.Form):
    ies = forms.CharField(label='ies', max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10000100'}))   # 看是否能改成int
    order_num = forms.CharField(label='order_num', max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CMCC-FS-SGYWTZ-***'}))
    client_num = forms.CharField(label='client_num', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2000411***'}))
    product_num = forms.CharField(label='product_num', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '20401074***'}))
    ip = forms.GenericIPAddressField(label='ip', protocol='both', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1.1.1.1'}))
    mask = forms.IntegerField(label='mask', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 24}))
    gateway = forms.CharField(label='gateway', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '183.*.*.*/24'}))
    link_tag = forms.IntegerField(label='link_tag', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 24}))
    device_name = forms.CharField(label='Device', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GDFOS-IPMAN-BNG01-DS-HW'}))
    logic_port = forms.CharField(label='logic_port', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'lag-10:1013.119'}))
    svlan = forms.CharField(label='svlan', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1013'}))
    cvlan = forms.CharField(label='cvlan', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '119'}))
    access_type = forms.CharField(label='access_type', max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PTN'}))
    olt_name = forms.CharField(label='olt', max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '佛山顺德容桂容奇邮局-OLT002-HW-MA5680T'}))
    client_name = forms.CharField(label='client_name', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '交通银行'}))
    ip_description = forms.CharField(label='description', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'O-INTER-FS-JiaoTongYinHangGuFenYouXianGongSiFSFH(20M)'}))
    up_brandwidth = forms.IntegerField(label='brandwidth(UP)', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 20}))
    down_brandwidth = forms.IntegerField(label='brandwidth(DOWN)', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 20}))
    # alc_time = forms.DateTimeField(auto_now_add=True)   # 自动填充

    def clean_gateway(self):
        gateway = self.cleaned_data['gateway']
        exp = r'(([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5]).){3}([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])/[0-9]{1,2}'
        if re.match(exp, gateway):
            return gateway
        else:
            raise forms.ValidationError('gateway input error.')

    # def clean_ip(self): # TODO:验证IP是否已经分配出去
    #     pass

class IpAdjustForm(forms.Form):
    adj_order = forms.CharField(label='client_name', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CMCC-FS-SGYWTZ-***'}))
    # adj_time = forms.DateTimeField(blank=True)    # 程序协助填充
    # user取request.user

class IpcloseForm(forms.Form):
    close_order = forms.CharField(label='client_name', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CMCC-FS-SGYWTZ-***'}))
    # close_time = forms.DateTimeField(blank=True)  # 程序协助填充
    # user取request.user