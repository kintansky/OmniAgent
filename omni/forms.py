from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
import datetime

class LoginForm(forms.Form):
    username = forms.CharField(label="User", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('User name or password error.') # 如果错误通过加入错误信息，返回给前端
        else:
            self.cleaned_data['user'] = user    # 返回的是user对象给views，不是username
        return self.cleaned_data

class RegisterForm(forms.Form):
    username = forms.CharField(min_length=5, max_length=30, label="User", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '姓名汉语拼音'}))
    first_name = forms.CharField(label="ZH_Name", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '中文姓名'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'example@example.example'}))
    password = forms.CharField(min_length=6, label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'at least 6 characters'}))
    password_again = forms.CharField(min_length=6, label="Password Again", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'at least 6 characters'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('User already exists')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already exists')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('password dosent match')
        return password_again


# TimeRangeForm可以作为其他需要选择时间的form的基类
class TimeRangeForm(forms.Form):
    time_begin = forms.DateTimeField(label='From', widget=forms.TextInput(attrs={'class': 'form-control form_datetime', 'placeholder': '2018-01-01 00:00:00', 'style':'width:160px', 'readonly': True}))
    time_end = forms.DateTimeField(label='to', widget=forms.TextInput(attrs={'class': 'form-control form_datetime', 'placeholder': '2018-01-11 23:59:59', 'style':'width:160px', 'readonly': True}))

    def clean(self):
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