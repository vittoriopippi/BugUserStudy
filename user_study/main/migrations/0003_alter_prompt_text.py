# Generated by Django 4.1.7 on 2023-11-09 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_answer_sample_a_remove_answer_sample_b_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prompt',
            name='text',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
