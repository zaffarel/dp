# Generated by Django 2.2 on 2020-10-30 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenarist', '0016_auto_20201029_0518'),
    ]

    operations = [
        migrations.AddField(
            model_name='act',
            name='full_id',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='drama',
            name='full_id',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='epic',
            name='full_id',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='event',
            name='full_id',
            field=models.CharField(default='', max_length=64),
        ),
    ]
