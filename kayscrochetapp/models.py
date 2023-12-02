from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Item(models.Model):
    item_title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='items_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='items_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='items_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='items_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pub_date = models.DateTimeField("date published")
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.item_title

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - timezone.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class LikeItem(models.Model):
    item_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Customerorder(models.Model):
    full_name = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.full_name}'s Order"

    class Meta:
        verbose_name = "Customer_Order"
        verbose_name_plural = "Customer_Orders"
