# Generated by Django 3.1.4 on 2020-12-17 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0005_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
