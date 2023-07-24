from django.db import models

class BuildHist(models.Model):
    component = models.CharField(max_length=50)
    lastupdtid = models.CharField(max_length=50)
    lastupdt = models.DateTimeField()