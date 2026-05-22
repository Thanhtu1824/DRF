from django.db import models

# Create your models here.
    
 
class Brand(models.Model):

    name = models.CharField(max_length=100)
    logo_url = models.URLField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        
        return self.name
    
