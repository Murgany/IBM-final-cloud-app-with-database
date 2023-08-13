# Generated by Django 4.1.7 on 2023-08-11 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlinecourse', '0002_choice_submission_question_choice_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='lesson',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_grade',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='lesson_exam',
        ),
        migrations.AddField(
            model_name='question',
            name='course',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='onlinecourse.course'),
        ),
        migrations.AddField(
            model_name='submission',
            name='course',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='onlinecourse.course'),
        ),
    ]
