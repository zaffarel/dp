# Generated by Django 2.2 on 2019-04-22 02:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='beneficeafflictionref',
            options={'ordering': ['category', 'reference']},
        ),
    ]
