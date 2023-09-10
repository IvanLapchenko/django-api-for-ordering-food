from django.db import models


class Printer(models.Model):
    CLIENT = 'client'
    KITCHEN = 'kitchen'
    TYPE_CHOICES = [
        (CLIENT, 'client'),
        (KITCHEN, 'kitchen'),
    ]

    name = models.CharField()
    api_key = models.CharField()
    check_type = models.CharField(choices=TYPE_CHOICES)
    point_id = models.IntegerField()


class Check(models.Model):
    NEW = 'new'
    RENDERED = 'rendered'
    PRINTED = 'printed'
    STATUS_CHOICES = [
        (NEW, 'new'),
        (RENDERED, 'rendered'),
        (PRINTED, 'printed')
    ]

    CLIENT = 'client'
    KITCHEN = 'kitchen'
    TYPE_CHOICES = [
        (CLIENT, 'client'),
        (KITCHEN, 'kitchen'),
    ]

    printer_id = models.ForeignKey(Printer, on_delete=models.PROTECT)
    type = models.CharField(choices=TYPE_CHOICES)
    order = models.JSONField()
    status = models.CharField(choices=STATUS_CHOICES, default=NEW)
    pdf_file = models.FileField(upload_to='')