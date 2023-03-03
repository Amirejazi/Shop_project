from django.db import models

class Order(models.Model):
    customer = models.ForeignKey(customer,)
