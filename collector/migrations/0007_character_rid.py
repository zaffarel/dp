# Generated by Django 2.0.2 on 2018-04-28 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0006_auto_20180428_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='rid',
            field=models.CharField(default='none', max_length=200),
        ),
    ]
