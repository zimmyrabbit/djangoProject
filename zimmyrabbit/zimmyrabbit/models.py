from django.db import models
from django.utils import timezone

class BuildHist(models.Model):
    env = models.CharField(max_length=50)
    component = models.CharField(max_length=50)
    lastupdtid = models.CharField(max_length=50)

    def get_current_time():
        return timezone.now
    
    lastupdt = models.DateTimeField(default=get_current_time)

    class Meta:
        unique_together = (("env", "component"),)