# Generated by Django 2.2.10 on 2020-05-11 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0005_auto_20200511_0328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipref',
            name='ship_shields',
            field=models.CharField(blank=True, choices=[('2', '2/2'), ('4', '4/4'), ('6', '6/6'), ('8', '8/8'), ('9', '9/9'), ('12', '12/12')], default='2/2', max_length=30),
        ),
    ]
