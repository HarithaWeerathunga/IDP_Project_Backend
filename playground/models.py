from django.db import models

# Create your models here.
class Drink(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    image = models.ImageField(null=True, blank=True, upload_to="image/")
    url = models.URLField(blank=True)
    
    def __str__(self):
        return self.name + ' ' + self.description
