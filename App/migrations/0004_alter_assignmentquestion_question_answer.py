# Generated by Django 4.2.6 on 2025-02-01 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_remove_course_instructor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentquestion',
            name='question_answer',
            field=models.CharField(max_length=1),
        ),
    ]
