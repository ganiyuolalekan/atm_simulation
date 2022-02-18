from django.db import models


class Customer(models.Model):
    id = models.AutoField(primary_key=True)

    full_name = models.CharField(max_length=100, unique=True)
    account_number = models.CharField(max_length=10, unique=True)
    amount = models.IntegerField()
    pin = models.CharField(max_length=4, unique=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.full_name)
