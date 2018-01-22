from django.db import models
from django.urls import reverse

class zipcsvfile(models.Model):
    filename        = models.CharField(max_length=32)
    path            = models.FileField()
    timesdownloaded = models.IntegerField(null=True, blank=True)
    timestamp       = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.filename
    def get_absolute_url(self):
        return reverse('scoretable:downloadzip', kwargs={'filename': self.filename})
