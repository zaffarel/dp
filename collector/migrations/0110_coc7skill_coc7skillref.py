# Generated by Django 2.2 on 2021-01-02 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0109_investigator_epic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coc7SkillRef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=200, unique=True)),
                ('smart_code', models.CharField(max_length=200, unique=True)),
                ('base', models.PositiveIntegerField(default=0)),
                ('era', models.CharField(max_length=4)),
                ('is_root', models.BooleanField(default=False)),
                ('is_speciality', models.BooleanField(default=False)),
                ('is_common', models.BooleanField(default=True)),
                ('is_wildcard', models.BooleanField(default=False)),
                ('linked_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='collector.Coc7SkillRef')),
            ],
            options={
                'verbose_name': 'COC7: Skill Reference',
                'ordering': ['is_speciality', 'is_wildcard', 'reference'],
            },
        ),
        migrations.CreateModel(
            name='Coc7Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField(default=0)),
                ('investigator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collector.Investigator')),
                ('skill_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collector.Coc7SkillRef')),
            ],
            options={
                'verbose_name': 'Investigators Skill',
                'ordering': ['skill_ref'],
            },
        ),
    ]
