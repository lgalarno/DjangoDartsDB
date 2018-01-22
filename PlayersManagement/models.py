from django.db import models
from django.urls import reverse

def upload_location(instance, filename):
    return "{0}/{1}".format(instance, filename)

# Create your models here.
class Player(models.Model):
    name        = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    picture     = models.ImageField( upload_to = upload_location,
                              null=True,
                              blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated     = models.DateTimeField(auto_now_add=False, auto_now=True)
    active      = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        #return "/player/{0}".format(self.name)
        return reverse('PlayersManagement:PlayerDetail', kwargs={'name': self.name})