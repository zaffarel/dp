# Generated by Django 2.0.2 on 2018-05-11 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0012_auto_20180505_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='ready_for_export',
            field=models.BooleanField(default=False),
        ),
    ]
