from django import forms
import re
from omni.forms import TimeRangeForm

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
class ClientSearchForm(forms.Form):
    order_num = forms.CharField(label='服开单号', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    group_id = forms.IntegerField(label='集团客户编号', required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    product_id = forms.IntegerField(label='产品编号', required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    client_name = forms.CharField(label='客户名称', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_client_name(self):
        return self.cleaned_data['client_name'].strip()
    
    def clean_order_num(self):
        return self.cleaned_data['order_num'].strip()


class IPAllocateSearchForm(ClientSearchForm):
    ip_address = forms.GenericIPAddressField(label='IP', protocol='both', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1.1.1.1'}))
    community = forms.CharField(label='Community', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_comminity(self):
        return self.cleaned_data['community'].strip()

class IPTargetForm(forms.Form):
    IPFUNC_CHOICES = (
        ('公网', '公网'),
        ('私网', '私网'),
        ('特殊', '特殊'),
    )
    STATE_CHOICES = (
        ('预分配', '预分配'),
        ('已启用', '已启用'),
        ('临时禁用', '临时禁用'),
    )
    ip_func = forms.ChoiceField(label='IP类型', choices=IPFUNC_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    state = forms.ChoiceField(label='状态', choices=STATE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    # first_ip = forms.GenericIPAddressField(label='起始IP', protocol='both', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%', 'placeholder': '192.168.1.4'}))
    first_ip = forms.CharField(label='IP', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%', 'placeholder': '192.168.1.4/24'}))
    ip_num = forms.IntegerField(label='往后', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:15%'}))
    ip_segment = forms.CharField(label='IP网段', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '192.168.1.0/24'}))
    gateway = forms.GenericIPAddressField(label='网关', protocol='both', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '192.168.1.1'}))
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     first_ip = cleaned_data.get('first_ip')
    #     ip_num = cleaned_data.get('ip_num')
    #     ip_segment = cleaned_data.get('ip_segment')
    #     if ip_segment == '':
    #         if first_ip == '' and ip_num is None:
    #             raise forms.ValidationError('IP地址段/(起始IP+IP数量)必填其一')
    #     else:
    #         if re.match(r'(\d+\.){3}\d+/\d{1,2}', ip_segment):
    #             if first_ip and ip_num:
    #                 raise forms.ValidationError('每次分配：IP地址段/(起始IP+IP数量)只填其一')
    #         else:
    #             raise forms.ValidationError('IP地址段格式有误，请参考192.168.1.0/24')
    def clean(self):
        cleaned_data = super().clean()
        first_ip = cleaned_data.get('first_ip')
        ip_num = cleaned_data.get('ip_num')
        m = re.match(r'(\d+\.){3}\d+/\d{1,2}', first_ip)
        if m is None:
            raise forms.ValidationError('IP地址段格式有误，请参考192.168.1.0/24')
        if ip_num is None:
            self.cleaned_data['ip_num'] = 0
        return self.cleaned_data

class NewIPAllocationForm(forms.Form):
    NET_CHOICES = (
        ('', ''),
        ('双上联', '双上联'),
        ('单上联', '单上联'),
    )
    ACCESS_CHOICES = (
        ('', ''),
        ('GPON', 'GPON'),
        ('PTN', 'PTN'),
        ('DIRECT', 'DIRECT'),
    )
    order_num = forms.CharField(label='服开单号', widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:70%'}))
    client_name = forms.CharField(label='客户名称', widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:70%'}))
    
    # olt与bng关系处理
    olt = forms.CharField(label='OLT/PTN', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入OLT中文名进行模糊匹配', 'style': 'width:70%'}))
    access_type = forms.ChoiceField(label='接入方式', choices=ACCESS_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'style': 'width:70%'}))
    bng = forms.CharField(label='BNG/SR', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '点击生成BNG，如系统无法匹配，请手工填入，多台设备间使用 / 分割', 'style': 'width:70%'}))
    # 子接口与内外层vlan关系
    # TODO: 确认下私网是否需要填写子接口
    logic_port = forms.CharField(label='子接口', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'lag-100:200.0 或 Eth-Trunk1:200.0', 'style': 'width:70%'}))
    # 描述与带宽的关系
    description = forms.CharField(label='描述', widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:70%'}))    
    service_id = forms.IntegerField(label='业务ID', widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:70%'}))
    group_id = forms.IntegerField(label='集团编码', widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:70%'}))
    product_id = forms.IntegerField(label='产品编码', widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:70%'}))
    network_type = forms.ChoiceField(label='组网类型', choices=NET_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'style': 'width:70%'}))

    # 其他信息
    INCLUDE_PRIVATE_CHOICES = (
        ('n', 'no'),
        ('y', 'yes'),
    )
    include_private_ip = forms.ChoiceField(label='包含私网地址', choices=INCLUDE_PRIVATE_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    comment = forms.CharField(label='备注', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '最多255个字符'}))
    # 私网信息，校验涉及两个form，在view中实现
    community = forms.CharField(label='COMMUNITY', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'community', 'style': 'width:70%'}))
    rt = forms.CharField(label='RT', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'rt', 'style': 'width:70%'}))
    rd = forms.CharField(label='RD', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'rd', 'style': 'width:70%'}))
    
    icp_id = forms.IntegerField(label='icp_id', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

    # 如果多字段同时clean只能使用clean，执行顺序是先单字段校验，再进行混合的clean
    def clean(self):
        cleaned_data = super().clean()
        access_type = cleaned_data.get('access_type')
        olt = cleaned_data.get('olt')
        if 'PTN' in olt.upper() and access_type != 'PTN':
            # raise forms.ValidationError('接入设备为PTN，但接入方式为{}'.format(olt))
            self.add_error('access_type', '接入设备为PTN，但接入方式为{}'.format(access_type))
        elif 'OLT' in olt.upper() and access_type != 'GPON':
            # raise forms.ValidationError('接入设备为OLT，但接入方式为{}'.format(olt))
            self.add_error('access_type', '接入设备为OLT，但接入方式为{}'.format(access_type))
        elif re.match(r'.*?(-BNG\d+)|(-BRAS\d+).*?', olt.upper()) and access_type != 'DIRECT':
            # raise forms.ValidationError('接入设备为BNG，但接入方式为{}'.format(olt))
            self.add_error('access_type', '接入设备为BNG，但接入方式为{}'.format(access_type))
        return cleaned_data

    def clean_olt(self):
        return self.cleaned_data['olt'].strip()

    def clean_access_type(self):
        if self.cleaned_data['access_type'] == '':
            raise forms.ValidationError('请选择接入类型')
        else:
            return self.cleaned_data['access_type']

    def clean_bng(self):
        bng = self.cleaned_data['bng']
        bngList = [b.strip() for b in bng.split('/') if b.strip() != '']    # 如果bng填写只有单台，而且/没去掉的情况，这里会处理掉
        return '/'.join(bngList)

    def clean_network_type(self):
        if self.cleaned_data['network_type'] == '':
            raise forms.ValidationError('请选择组网类型')
        else:
            return self.cleaned_data['network_type']

    def clean_group_id(self):
        group_id = self.cleaned_data['group_id']
        num_cnt = 10
        if group_id / (10**(num_cnt-1)) < 1:
            raise forms.ValidationError('集团编码位数应>={}位'.format(num_cnt))
        else:
            return group_id

    def clean_product_id(self):
        product_id = self.cleaned_data['product_id']
        num_cnt = 10
        if product_id / (10**(num_cnt-1)) < 1:
            raise forms.ValidationError('产品编码位数应>={}位'.format(num_cnt))
        else:
            return product_id
    
    def clean_order_num(self):
        # TODO: 增加检验
        return self.cleaned_data['order_num'].strip()

    def clean_client_name(self):
        return self.cleaned_data['client_name'].strip()
    
    def clean_logic_port(self):
        logic_port = self.cleaned_data['logic_port'].strip()
        logic_port = logic_port.replace('：', ':')
        m = re.match(r'([^:\.]+):(\d+)\.(\d+)', logic_port)
        if m:
            logic_port = m.group(1)
            self.cleaned_data['svlan'] = int(m.group(2))
            self.cleaned_data['cevlan'] = int(m.group(3))
            return logic_port
        else:
            raise forms.ValidationError('子接口规范应为 端口:外层vlan.内层vlan, 如无内外层vlan请使用**:0.0的格式')
    
    def clean_description(self):
        ip_description = self.cleaned_data['description'].strip()    # 去错误输入的无用字符
        ip_description = ip_description.replace('（', '(')
        ip_description = ip_description.replace('）', ')')
        exp = r'.*?\((\d*)(M|G)\)'
        m = re.match(exp, ip_description, re.I)
        if m:
            if m.group(2).upper() == 'M':
                self.cleaned_data['brand_width'] = int(m.group(1))
            elif m.group(2).upper() == 'G':
                self.cleaned_data['brand_width'] = int(m.group(1))*1024
            return ip_description
        else:
            raise forms.ValidationError('描述规范应为 abcdefg(**M)或abcdefg(**G),包含带宽字段')

    def clean_comment(self):
        return self.cleaned_data['comment'].strip()

    def clean_community(self):
        community = self.cleaned_data['community'].strip()
        if self.cleaned_data['include_private_ip'] == 'y':
            if community == '':
                raise forms.ValidationError('分配目标地址包含私网地址，请填写community')
            else:
                return community

    def clean_rt(self):
        rt = self.cleaned_data['rt'].strip()
        if self.cleaned_data['include_private_ip'] == 'y':
            if rt == '':
                raise forms.ValidationError('分配目标地址包含私网地址，请填写rt')
            else:
                return rt

    def clean_rd(self):
        rd = self.cleaned_data['rd'].strip()
        if self.cleaned_data['include_private_ip'] == 'y':
            if rd == '':
                raise forms.ValidationError('分配目标地址包含私网地址，请填写rd')
            else:
                return rd

    def clena_service_id(self):
        service_id = self.cleaned_data['service_id']
        num_cnt = 10
        if service_id/(10**(num_cnt+1)) > 1:
            raise forms.ValidationError('service id位数应<={}位'.format(num_cnt))
        else:
            return service_id


class ICPInfoForm(forms.Form):
    identify_id = forms.CharField(label='单位证件号码', required=False, widget=forms.TextInput(attrs={'class': 'form-control input-sm', 'placeholder': '营业执照号',}))
    guard_level = forms.CharField(label='业务保障等级', required=False, widget=forms.TextInput(attrs={'class': 'form-control input-sm', 'placeholder': '保护等级',}))
    city = forms.CharField(label='受理地市', required=False, widget=forms.TextInput(attrs={'class': 'form-control input-sm',}))
    district = forms.CharField(label='受理区域', required=False, widget=forms.TextInput(attrs={'class': 'form-control input-sm',}))
    distributor = forms.CharField(label='派单人', required=False, widget=forms.TextInput(attrs={'class': 'form-control input-sm',}))
    distributor_contact = forms.CharField(label='派单人联系方式', required=False, widget=forms.TextInput(attrs={'class': 'form-control input-sm',}))
    demand = forms.CharField(label='需求描述', required=False, widget=forms.TextInput(attrs={'class': 'form-control input-sm',}))
    bandwidth_up = forms.IntegerField(label='上行带宽M', min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control input-sm', 'placeholder': '20M'}))
    bandwidth_dwn = forms.IntegerField(label='下行带宽M', min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control input-sm', 'placeholder': '20M'}))
    client_tech = forms.CharField(label='客户配合联系人', required=False, widget=forms.TextInput(attrs={'class': 'form-control input-sm',}))
    client_tech_contact = forms.CharField(label='客户配合联系方式', required=False, widget=forms.TextInput(attrs={'class': 'form-control input-sm',}))
    demand_ipv4_amount = forms.IntegerField(label='IPV4数量', min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control input-sm',}))
    demand_ipv6_amount = forms.IntegerField(label='IPV6数量', min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control input-sm',}))
    client_address = forms.CharField(label='单位详细地址', required=False, widget=forms.TextInput(attrs={'class': 'form-control input-sm',}))
    businessman = forms.CharField(label='联系人姓名（客户侧）', required=False, widget=forms.TextInput(attrs={'class': 'form-control input-sm',}))
    businessman_contact = forms.CharField(label='联系人电话（客户侧）', required=False, widget=forms.TextInput(attrs={'class': 'form-control input-sm',}))


class DeviceIpSegmentForm(forms.Form):
    device_name = forms.CharField(label='Device', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GDFOS-IPMAN-BNG01-DS-HW', 'style':'width:200px'}))


class NewIpSegmentForm(forms.Form):
    SEGMENT_STATE_CHOICES = (
        (0, '未启用'),
        (1, '启用'),
    )
    segment = forms.GenericIPAddressField(label='IP', protocol='both', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '192.168.1.0', 'style': 'width:80%'}))
    mask = forms.IntegerField(label='掩码', widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:50%'}))
    segment_state = forms.ChoiceField(label='状态', choices=SEGMENT_STATE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

class NewSchemaSegmentForm(forms.Form):
    SEGMENT_SPECIALIZATION_CHOICES = (
        ('网吧', '网吧'),
        ('专线', '专线'),
        ('其他', '其他'),
    )
    segment = forms.CharField(label='网段', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '192.168.1.0/24', 'style': 'width:80%', }))
    specialization = forms.ChoiceField(label='专业', choices=SEGMENT_SPECIALIZATION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    def clean_segment(self):
        d = self.cleaned_data['segment'].strip()
        if re.match(r'(\d+\.){3}\d+/\d{1,2}', d):
            return d
        else:
            raise forms.ValidationError('目标网段格式有误，请正确填写')

class NewDraftSegmentBaseForm(forms.Form):
    ACCESS_CHOICES = (
        ('', ''),
        ('GPON', 'GPON'),
        ('PTN', 'PTN'),
        ('DIRECT', 'DIRECT'),
    )
    DRAFT_TYPE_CHOICES = (
        ('1', '根据需求IP数量规划'),
        ('2', '根据网段IP掩码规划'),
    )
    DRAFT_TYPE_ADDON_CHOICES = (
        ('1', '只生成一个子网段'),
        ('2', '生成所有子网段'),
    )
    # 搜索框
    search_olt = forms.CharField(label='输入搜索OLT', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    search_bng = forms.CharField(label='输入搜索BNG', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # 填充框
    access_olt = forms.CharField(label='接入OLT', widget=forms.TextInput(attrs={'class': 'form-control'}))
    access_bng = forms.CharField(label='接入BNG', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    access_type = forms.ChoiceField(label='接入方式', choices=ACCESS_CHOICES, widget=forms.Select(attrs={'class': 'forms-control'}))
    draft_type = forms.ChoiceField(label='规划方式', choices=DRAFT_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'forms-control'}))
    draft_type_addon = forms.ChoiceField(label='分配方式', required=False, disabled=True, choices=DRAFT_TYPE_ADDON_CHOICES, widget=forms.Select(attrs={'class': 'forms-control'}))
    gateway = forms.GenericIPAddressField(label='网关', required=False, protocol='both', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '如192.168.1.1，如未指定默认使用子网段的第一个IP作为网关'}))
    amount = forms.IntegerField(label='需求数量or掩码', max_value=256, min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '如通过掩码规划，请填掩码，如通过数量规划，请填写数量'}))

    def clean(self):
        cleaned_data = super().clean()
        access_type = cleaned_data.get('access_type')
        olt = cleaned_data.get('access_olt')
        bng = cleaned_data.get('access_bng')
        if olt is not None:
            if 'PTN' in olt.upper() and access_type != 'PTN':
                self.add_error('access_type', '接入设备为PTN，但接入方式为{}'.format(access_type))
            elif 'OLT' in olt.upper() and access_type != 'GPON':
                self.add_error('access_type', '接入设备为OLT，但接入方式为{}'.format(access_type))
            elif olt == '' and re.match(r'.*?(-BNG\d+)|(-BRAS\d+)|(-SR\d+).*?', bng.upper()) and access_type != 'DIRECT':
                self.add_error('access_type', '接入设备为BNG，但接入方式为{}'.format(access_type))
        draft_type = cleaned_data.get('draft_type')
        amount = cleaned_data.get('amount')
        if draft_type == '2' and amount > 32:
            self.add_error('amount', '根据网段IP掩码规划情况下，掩码可选范围为[0, 32]')
        return cleaned_data

    def clean_access_type(self):
        if self.cleaned_data['access_type'] == '' or self.cleaned_data['access_type'] is None:
            raise forms.ValidationError('未选择接入方式')
        else:
            return self.cleaned_data['access_type']

class WorkLoadSearchForm(TimeRangeForm):
    worker = forms.CharField(label='用户', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_worker(self):
        return self.cleaned_data['worker'].strip()