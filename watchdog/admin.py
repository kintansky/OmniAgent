from django.contrib import admin
from .models import DeviceManufactor, Device, CommandLine

# Register your models here.
# User/PS: django_admin/root1234
@admin.register(DeviceManufactor)
class DeviceManufactorAdmin(admin.ModelAdmin):
    list_display = ('manufactor_name',)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'device_ip', 'device_manufactor', 'device_network')

@admin.register(CommandLine)
class CommandLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'cmd_manufactor', 'cmd_func', 'cmd_content', 'cmd_description')
