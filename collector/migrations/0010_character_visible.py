# Generated by Django 2.1 on 2019-03-02 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0009_auto_20190224_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='visible',
            field=models.BooleanField(default=False),
        ),
    ]
