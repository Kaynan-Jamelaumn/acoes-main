# Generated by Django 5.0.2 on 2024-04-02 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_student_previous_school_student_school_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='region',
        ),
        migrations.AddField(
            model_name='institute',
            name='region',
            field=models.CharField(default='xue hua piao', max_length=150),
            preserve_default=False,
        ),
    ]