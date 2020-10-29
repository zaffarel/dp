# Generated by Django 2.2 on 2020-10-24 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scenarist', '0006_auto_20201024_1506'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quizzanswer',
            options={'ordering': ['question', 'num']},
        ),
        migrations.CreateModel(
            name='Quizz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.PositiveIntegerField(default=1)),
                ('ally', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ally', to='scenarist.QuizzAnswer')),
                ('associated_story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scenarist.Drama')),
                ('goal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='goal', to='scenarist.QuizzAnswer')),
                ('patron', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patron', to='scenarist.QuizzAnswer')),
                ('twist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='twist', to='scenarist.QuizzAnswer')),
                ('villain', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='villain', to='scenarist.QuizzAnswer')),
            ],
        ),
    ]
