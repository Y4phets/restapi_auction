# Generated by Django 3.1.4 on 2020-12-17 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0006_auto_20201217_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='rate',
            field=models.PositiveIntegerField(default=0, help_text='указывать сумму в долларах', verbose_name='Cтавка'),
        ),
    ]
