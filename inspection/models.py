from django.db import models

# Create your models here.
class OpticalMoudleDiff(models.Model):
    device_name = models.CharField(max_length=255)
    port = models.CharField(max_length=40)
    now_moudle = models.CharField(max_length=60)
    ever_moudle = models.CharField(max_length=60)
    STATUS_CHOICES = (
        ('NEW', 'plugin'),
        ('MISS', 'missing'),
        ('CH', 'changed'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    record_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-record_time']