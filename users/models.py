from django.db import models

# Create your models here.
class Act(models.Model):
    """
    アカウント情報
    """
    act_id = models.CharField(max_length=10)
    password = models.CharField(null=False, blank=False, max_length=4000)
    first_name = models.CharField(null=True, blank=True, max_length=10)
    last_name = models.CharField(null=True, blank=True, max_length=10)
    short_name = models.CharField(null=True, blank=True, max_length=8)
    birthday = models.DateTimeField(null=True, blank=True)
    gender = models.IntegerField(null=True, blank=True)
    mail_address = models.CharField(null=True, blank=True, max_length=254)
    phone_number = models.CharField(null=True, blank=True, max_length=15)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
