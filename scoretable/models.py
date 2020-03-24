from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class zipcsvfile(models.Model):
    filename        = models.CharField(max_length=32)
    slug            = models.SlugField(max_length=32)
    path            = models.FileField()
    timesdownloaded = models.IntegerField(null=True, blank=True)
    timestamp       = models.DateTimeField(auto_now_add=True, auto_now=False)
    class Meta:
        ordering = ('-timestamp',)
    def __str__(self):
        return self.filename
    def get_absolute_url(self):
        return reverse('scoretable:downloadzip', kwargs={'slug': self.slug})
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.filename)
        super(zipcsvfile, self).save(*args, **kwargs)