# Generated by Django 3.2.7 on 2021-09-26 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='quizresult',
            unique_together={('quiz_id', 'question_id', 'user_id', 'answer')},
        ),
    ]
