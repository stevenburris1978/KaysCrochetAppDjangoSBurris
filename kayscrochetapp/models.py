from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone


class Item(models.Model):
    item_title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='items/images/', blank=True, null=True)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.item_title

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
