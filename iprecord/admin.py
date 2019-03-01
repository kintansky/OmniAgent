from django.contrib import admin
from .models import PublicIpRecord

# Register your models here.
@admin.register(PublicIpRecord)
class PublicIpRecordAdmin(admin.ModelAdmin):
    list_display = ('device_ip', 'device_name', 'logic_port', 'svlan', 'cvlan', 'ip_description')