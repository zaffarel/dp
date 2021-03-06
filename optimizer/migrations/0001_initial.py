# Generated by Django 2.2 on 2021-03-04 03:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('collector', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('public', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TeamMate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collector.Character')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='optimizer.Team')),
            ],
        ),
    ]
