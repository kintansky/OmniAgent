from django.contrib import admin
from .models import PublicIpSegment

# Register your models here.
@admin.register(PublicIpSegment)
class PublicIpSegmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip_segment', 'mask', 'segment_type')
