# Generated by Django 4.2.4 on 2023-08-12 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinecourse', '0005_question_question_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_grade',
            field=models.FloatField(default=50.0),
        ),
    ]
