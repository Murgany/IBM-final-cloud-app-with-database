# Generated by Django 4.2.4 on 2023-08-12 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinecourse', '0004_alter_question_course_alter_submission_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_grade',
            field=models.CharField(default=10, max_length=10),
        ),
    ]