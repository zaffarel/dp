# Generated by Django 2.2.7 on 2020-04-15 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0045_auto_20200415_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourofdutyref',
            name='category',
            field=models.CharField(blank=True, choices=[('0', 'Birthright'), ('5', 'Balance'), ('10', 'Upbringing'), ('20', 'Apprenticeship'), ('30', 'Early Career'), ('40', 'Tour of Duty'), ('50', 'Worldly Benefits'), ('60', 'Nameless Kit')], default='Tour of Duty', max_length=20),
        ),
    ]
