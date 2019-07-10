from django import forms
import re

class IPsearchForm(forms.Form):
    CHOICES = (
        ('public_outer', '公网外部使用'),
        ('public_inner', '公网内部使用'),
        ('private', '私网'),
        ('all', '所有'),
    )
    ip_address = forms.GenericIPAddressField(label='IP', protocol='both', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1.1.1.1', 'style':'width:120px'}))
    device_name = forms.CharField(label='Device', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GDFOS-IPMAN-BNG01-DS-HW', 'style':'width:200px'}))
    description = forms.CharField(label='Description', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '...NanHai...', 'style':'width:200px'}))
    ip_type = forms.ChoiceField(label='Type', choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'style':'width:80px'}))

    def clean(self):
        cleaned_data = super().clean()
        ip_address = cleaned_data.get('ip_address')
        device_name = cleaned_data.get('device_name')
        description = cleaned_data.get('description')
        # if ip_address == device_name == description == '':
        #     raise forms.ValidationError('搜索字段：至少指定一个字段')
        # 不再限制，什么都不提供返回全部内容
        return self.cleaned_data


# IP 分配操作相关
class IPAllocateSearchForm(forms.Form):
    ip_address = forms.GenericIPAddressField(label='IP', protocol='both', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1.1.1.1', 'style':'width:150px'}))
    client_name = forms.CharField(label='ClientName', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '**公司', 'style':'width:300px'}))

    def clean_client_name(self):
        return self.cleaned_data['client_name'].strip()
        
class IpAllocateForm(forms.Form):
    CHOICES = (
        ('GPON', 'GPON'),
        ('PTN', 'PTN'),
    )
    CHOICES2 = (
        ('InUse', '在用'), # 在用
        ('ShutDown', '暂时关停'),   # 暂时关停
        ('Delete', '删除数据'),   # 删除数据
    )
    ies = forms.CharField(label='ies', max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '10000100'}))   # 看是否能改成int
    order_num = forms.CharField(label='工单号', max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': 'CMCC-FS-SGYWTZ-***'}))
    client_num = forms.CharField(label='集团客户编号 *', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '2000411***'}))
    product_num = forms.CharField(label='集团产品号码 *', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '20401074***'}))
    ip = forms.GenericIPAddressField(label='IP *', protocol='both', widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '1.1.1.1'}))
    # mask = forms.IntegerField(label='掩码', widget=forms.NumberInput(attrs={'class': 'form-control allocate', 'placeholder': 24}))
    gateway = forms.CharField(label='网关 *', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '183.*.*.*/24'}))
    link_tag = forms.IntegerField(label='链路标识', required=False, widget=forms.NumberInput(attrs={'class': 'form-control allocate', 'placeholder': 2}))
    device_name = forms.CharField(label='SR/BNG/BRAS *', widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': 'GDFOS-IPMAN-BNG01-DS-HW'}))
    # svlan = forms.CharField(label='外层vlan', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '1013'}))
    # cvlan = forms.CharField(label='内层vlan', max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '119'}))
    access_type = forms.ChoiceField(label='接入类型', choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control allocate'}))
    # access_type = forms.CharField(label='接入类型', max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': 'PTN'}))
    logic_port = forms.CharField(label='子接口 *', widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': 'lag-10:1013.119或Eth-Trunk107.2603.105'}))
    olt_name = forms.CharField(label='olt', max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '佛山顺德容桂容奇邮局-OLT002-HW-MA5680T'}))
    client_name = forms.CharField(label='客户名称 *', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '交通银行'}))
    ip_description = forms.CharField(label='描述', required=False, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': 'O-INTER-FS-JiaoTongYinHangGuFenYouXianGongSiFSFH(20M)'}))
    up_brandwidth = forms.IntegerField(label='带宽(UP)', required=False, widget=forms.NumberInput(attrs={'class': 'form-control allocate', 'placeholder': 20}))
    # down_brandwidth = forms.IntegerField(label='带宽(DOWN) *', widget=forms.NumberInput(attrs={'class': 'form-control allocate', 'placeholder': 20}))
    state = forms.ChoiceField(label='状态 *', choices=CHOICES2, widget=forms.Select(attrs={'class': 'form-control allocate'}))


    def clean_device_name(self):
        device_name = self.cleaned_data['device_name'].strip()
        return device_name
    
    def clean_olt_name(self):
        olt_name = self.cleaned_data['olt_name'].strip()
        return olt_name

    def clean_gateway(self):
        gateway = self.cleaned_data['gateway']
        exp = r'(([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5]).){3}([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])/([1-9]\d)'
        m = re.match(exp, gateway)
        if m:
            self.cleaned_data['mask'] = int(m.group(4))
            return gateway
        else:
            raise forms.ValidationError('gateway input error.')
    
    def clean_ip_description(self):
        ip_description = self.cleaned_data['ip_description'].strip()    # 去错误输入的无用字符
        exp = r'.*?\((\d*)(M|G)\)'
        m = re.match(exp, ip_description)
        if m:
            if m.group(2) == 'M':
                self.cleaned_data['down_brandwidth'] = int(m.group(1))
            elif m.group(2) == 'G':
                self.cleaned_data['down_brandwidth'] = int(m.group(1))*1024
            return ip_description
        else:
            raise forms.ValidationError('请规范填写描述字段：如abcdefg(**M)或abcdefg(**G)，详见右下角填写帮助')

    def clean_logic_port(self):
        access_type = self.cleaned_data['access_type']
        logic_port = self.cleaned_data['logic_port'].strip()
        if access_type == 'PTN':
            m1 = re.match(r'lag-\d*:(\d*)', logic_port)
            if m1:
                self.cleaned_data['svlan'] = int(m1.group(1))
                self.cleaned_data['cvlan'] = 0
                return logic_port
            else:
                m2 = re.match(r'(\d{1,2}/){1,}\d{1,2}:(\d*)', logic_port)
                if m2:
                    self.cleaned_data['svlan'] = int(m2.group(2))
                    self.cleaned_data['cvlan'] = 0
                    return logic_port
        elif access_type == 'GPON':
            m1 = re.match(r'lag-\d+:(\d*)\.(\d*)', logic_port)
            if m1:
                self.cleaned_data['svlan'] = int(m1.group(1))
                self.cleaned_data['cvlan'] = int(m1.group(2))
                return logic_port
            else:
                m2 = re.match(r'(Eth-Trunk\d*\.(\d*))\.(\d*)', logic_port)
                if m2:
                    self.cleaned_data['svlan'] = int(m2.group(2))
                    self.cleaned_data['cvlan'] = int(m2.group(3))
                    return m2.group(1)
                else:
                    m3 = re.match(r'((\d{1,2}/){1,}\d{1,2}):(\d*).(\d*)', logic_port)
                    if m3:
                        self.cleaned_data['svlan'] = int(m3.group(3))
                        self.cleaned_data['cvlan'] = int(m3.group(4))
                        return m3.group(1)
        # 其他额外情况
        raise forms.ValidationError('请规范填写子接口，详见右下角填写帮助')

# 修改记录信息
class IpModForm(forms.Form):
    mod_order = forms.CharField(label='调整单号 *', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': 'CMCC-FS-SGYWTZ-***'}))
    mod_msg = forms.CharField(label='调整信息 *', widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '请简要填写调整的内容'}))

    def clean_mod_order(self):
        mod_order = self.cleaned_data['mod_order'].strip()
        if any(mod_order):
            return mod_order
        else:
            raise forms.ValidationError('变更或销户请填写变更单号')

    def clean_mod_msg(self):
        mod_msg = self.cleaned_data['mod_msg'].strip()
        return mod_msg

class IpPrivateAllocateForm(forms.Form):
    CHOICES = (
        ('GPON', 'GPON'),
        ('PTN', 'PTN'),
        ('VPN', 'VPN'),
    )
    CHOICES2 = (
        ('InUse', '在用'), # 在用
        ('ShutDown', '暂时关停'),   # 暂时关停
        ('Delete', '删除数据'),   # 删除数据
    )
    service = forms.CharField(label='业务标识', required=False, widget=forms.TextInput(attrs={'class': 'form-control allocate'}))   # 看是否能改成int
    community = forms.CharField(label='community', required=False, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': 'GDFS_JiaHeIPPBX'}))
    service_id = forms.CharField(label='service_id', required=False, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '20000100'}))
    rd = forms.CharField(label='rd *', widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '65277:660001'}))
    rt = forms.CharField(label='rt *', widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '65277:66000100'}))
    order_num = forms.CharField(label='接入依据', max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': 'CMCC-FS-SGYWTZ-***'}))
    client_name = forms.CharField(label='客户名 *', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '交通银行'}))
    client_num = forms.CharField(label='集团客户编号 *', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '2000411***'}))
    product_num = forms.CharField(label='集团产品号码 *', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '20401074***'}))
    device_name = forms.CharField(label='SR/BNG/BRAS *', widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': 'GDFOS-IPMAN-BNG01-DS-HW'}))
    access_type = forms.ChoiceField(label='接入方式', choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control allocate'}))
    logic_port = forms.CharField(label='子接口 *', widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': 'lag-10:1013.119'}))
    # svlan = forms.CharField(label='外层vlan *', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '1013'}))
    # cvlan = forms.CharField(label='内层vlan *', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '119'}))
    olt_name = forms.CharField(label='olt', max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '佛山顺德容桂容奇邮局-OLT002-HW-MA5680T'}))
    ip = forms.GenericIPAddressField(label='ip *', protocol='both', widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '1.1.1.1'}))
    gateway = forms.GenericIPAddressField(label='网关', protocol='both', required=False, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '183.*.*.*'}))
    ipsegment = forms.CharField(label='地址段', required=False, widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '183.*.*.*/24'}))
    ip_description = forms.CharField(label='描述 *', widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': 'I-VPN-FS-SS_XiNanAoYingGuangChang_OLT002_FoShanGongDianJu'}))
    state = forms.ChoiceField(label='状态 *', choices=CHOICES2, widget=forms.Select(attrs={'class': 'form-control allocate'}))

    def clean_ipsegment(self):
        ipsegment = self.cleaned_data['ipsegment']
        if any(ipsegment):
            exp = r'(([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5]).){3}([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])/[0-9]{1,2}'
            if re.match(exp, ipsegment):
                return ipsegment
            else:
                raise forms.ValidationError('ipsegment input error.')

    def clean_logic_port(self):
        access_type = self.cleaned_data['access_type']
        logic_port = self.cleaned_data['logic_port'].strip()
        if access_type == 'PTN':
            m1 = re.match(r'lag-\d*:(\d*)', logic_port)
            if m1:
                self.cleaned_data['svlan'] = int(m1.group(1))
                self.cleaned_data['cvlan'] = 0
                return logic_port
            else:
                m2 = re.match(r'(\d{1,2}/){1,}\d{1,2}:(\d*)', logic_port)
                if m2:
                    self.cleaned_data['svlan'] = int(m2.group(2))
                    self.cleaned_data['cvlan'] = 0
                    return logic_port
        elif access_type == 'GPON' or access_type == 'VPN':
            m1 = re.match(r'lag-\d+:(\d*)\.(\d*)', logic_port)
            if m1:
                self.cleaned_data['svlan'] = int(m1.group(1))
                self.cleaned_data['cvlan'] = int(m1.group(2))
                return logic_port
            else:
                m2 = re.match(r'(Eth-Trunk\d*\.(\d*))\.(\d*)', logic_port)
                if m2:
                    self.cleaned_data['svlan'] = int(m2.group(2))
                    self.cleaned_data['cvlan'] = int(m2.group(3))
                    return m2.group(1)
                else:
                    m3 = re.match(r'((\d{1,2}/){1,}\d{1,2}):(\d*).(\d*)', logic_port)
                    if m3:
                        self.cleaned_data['svlan'] = int(m3.group(3))
                        self.cleaned_data['cvlan'] = int(m3.group(4))
                        return m3.group(1)
        # 其他额外情况
        raise forms.ValidationError('请规范填写子接口，详见右下角填写帮助')


class IPTargetForm(forms.Form):
    IPFUNC_CHOICES = (
        ('私网', '私网'),
        ('公网', '公网'),
        ('特殊', '特殊'),
    )
    STATE_CHOICES = (
        ('预分配', '预分配'),
        ('已启用', '已启用'),
        ('已停用', '已停用'),
    )
    ip_func = forms.ChoiceField(label='IP类型', choices=IPFUNC_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    ip = forms.GenericIPAddressField(label='起始IP', protocol='both', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '192.168.1.4'}))
    ip_num = forms.IntegerField(label='IP数量', widget=forms.NumberInput(attrs={'class': 'form-control', 'value': 1}))
    # gateway = forms.GenericIPAddressField(label='网关', protocol='both', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '192.168.1.1'}))
    state = forms.ChoiceField(label='状态', choices=STATE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))


class NewIPAllocationForm(forms.Form):
    NET_CHOICES = (
        ('双上联', '双上联'),
        ('单上联', '单上联'),
    )
    order_num = forms.CharField(label='服开单号', widget=forms.TextInput(attrs={'class': 'form-control allocate'}))
    client_name = forms.CharField(label='客户名称', widget=forms.TextInput(attrs={'class': 'form-control allocate'}))
    # ip_func = forms.ChoiceField(label='IP类型', choices=IPFUNC_CHOICES, widget=forms.Select(attrs={'class': 'form-control allocate'}))
    # ip = forms.GenericIPAddressField(label='起始IP', protocol='both', widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '192.168.1.4'}))
    # ip_num = forms.IntegerField(label='IP数量', widget=forms.NumberInput(attrs={'class': 'form-control allocate'}))
    # gateway = forms.GenericIPAddressField(label='网关', protocol='both', widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': '192.168.1.1'}))

    # 子接口与内外层vlan关系
    logic_port = forms.CharField(label='子接口', widget=forms.TextInput(attrs={'class': 'form-control allocate', 'placeholder': 'lag-100.200.0 或 Eth-Trunk1.200.0'}))
    # svlan = forms.IntegerField(label='外层VLAN', widget=forms.NumberInput(attrs={'class': 'form-control allocate'}))
    # cevlan = forms.IntegerField(label='内层VLAN', widget=forms.NumberInput(attrs={'class': 'form-control allocate'}))
    
    # 描述与带宽的关系
    description = forms.CharField(label='描述', widget=forms.TextInput(attrs={'class': 'form-control allocate'}))
    # brand_width = forms.IntegerField(label='带宽', widget=forms.NumberInput(attrs={'class': 'form-control allocate'}))
    
    # olt与bng关系处理
    olt = forms.CharField(label='OLT', widget=forms.TextInput(attrs={'class': 'form-control allocate'}))
    bng = forms.CharField(label='BNG/SR', widget=forms.TextInput(attrs={'class': 'form-control allocate'}))

    service_id = forms.IntegerField(label='业务ID', widget=forms.NumberInput(attrs={'class': 'form-control allocate'}))
    group_id = forms.IntegerField(label='集团客户编号', widget=forms.NumberInput(attrs={'class': 'form-control allocate'}))
    client_id = forms.IntegerField(label='集团产品编号', widget=forms.NumberInput(attrs={'class': 'form-control allocate'}))
    network_type = forms.ChoiceField(label='组网类型', choices=NET_CHOICES, widget=forms.Select(attrs={'class': 'form-control allocate'}))

    # 其他信息
    comment = forms.CharField(label='备注', required=False, widget=forms.TextInput(attrs={'class': 'form-control allocate'}))


class PrivateIPExtraForm(forms.Form):   # 不要单独使用，需配合NewIPAllocationForm使用
    # 私网IP的额外信息
    community = forms.CharField(label='COMMUNITY', required=False, widget=forms.TextInput(attrs={'class': 'form-control allocate'}))
    rt = forms.CharField(label='RT', required=False, widget=forms.TextInput(attrs={'class': 'form-control allocate'}))
    rd = forms.CharField(label='RD', required=False, widget=forms.TextInput(attrs={'class': 'form-control allocate'}))