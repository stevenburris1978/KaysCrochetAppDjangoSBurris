# Generated by Django 5.0rc1 on 2023-12-03 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kayscrochetapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='items_images/'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='items_images/'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='items_images/'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to='items_images/'),
        ),
    ]
