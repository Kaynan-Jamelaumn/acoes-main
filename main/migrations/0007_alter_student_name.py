# Generated by Django 5.0.2 on 2024-03-25 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_course_modality_alter_course_shift'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
