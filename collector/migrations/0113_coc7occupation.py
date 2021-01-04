# Generated by Django 2.2 on 2021-01-02 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0112_auto_20210102_2324'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coc7Occupation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=200, unique=True)),
                ('smart_code', models.CharField(default='TBD', max_length=200)),
                ('is_classic', models.BooleanField(default=False)),
                ('is_lovecraftian', models.BooleanField(default=False)),
                ('occupation_points', models.CharField(choices=[('METHOD_1', 'EDU x 4'), ('METHOD_2', 'EDU x 2 + DEX x 2'), ('METHOD_3', 'EDU x 2 + APP x 2'), ('METHOD_4', 'EDU x 2 + FOR x 2'), ('METHOD_5', 'EDU x 2 + (DEX x 2 ou FOR x 2)'), ('METHOD_6', 'EDU x 2 + (DEX x 2 ou POU x 2)'), ('METHOD_7', 'EDU x 2 + (APP x 2 ou DEX x 2)'), ('METHOD_8', 'EDU x 2 + (APP x 2 ou POU x 2)'), ('METHOD_9', 'EDU x 2 + (APP x 2 ou DEX x 2 ou FOR x 2)')], default='METHOD_1', max_length=128)),
                ('credit_range', models.CharField(default='0;99', max_length=128)),
            ],
            options={
                'verbose_name': 'COC7: Occupation',
                'ordering': ['reference'],
            },
        ),
    ]
