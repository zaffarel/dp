# Generated by Django 2.2 on 2021-01-05 00:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0118_coc7skillmodificator'),
    ]

    operations = [
        migrations.AddField(
            model_name='investigator',
            name='occupation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='collector.Coc7Occupation'),
        ),
    ]
