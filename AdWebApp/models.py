from django.db import models


class PaperInput(models.Model):
    paperInput = models.CharField(max_length=2000)

class AdOutput(models.Model):
    paperOutput = models.CharField(max_length=2000)
    adList = models.CharField(max_length=2000)

class Ad(models.Model):
    title = models.CharField(max_length=200)
    price = models.CharField(max_length=20)
    link = models.CharField(max_length=200)