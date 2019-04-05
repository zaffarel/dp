# Generated by Django 2.1 on 2019-04-04 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0008_character_use_only_entrance'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='alliance_picture',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
        migrations.AddField(
            model_name='character',
            name='picture',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
    ]
