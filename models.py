from django.db import models

# Create your models here.
class Check(models.Model):
    dcheck = models.BooleanField(default=False)
    checkcsv = models.BooleanField(default=False)

    def __repr__(self):
        return 'choice ' + str(self.id) 