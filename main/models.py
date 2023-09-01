from django.db import models


class Order(models.Model):
    order_number = models.CharField(max_length=100)
    order_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_number


class Check(models.Model):
    CLIENT = 'client'
    KITCHEN = 'kitchen'
    TYPE_CHOICES = [
        (CLIENT, 'client'),
        (KITCHEN, 'kitchen'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pdf_link = models.FileField(upload_to='media/pdf')
    status = models.CharField(max_length=50)
    type = models.CharField(max_length=8, choices=TYPE_CHOICES)
