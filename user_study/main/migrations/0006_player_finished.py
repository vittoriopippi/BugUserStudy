# Generated by Django 4.2.7 on 2023-11-14 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_player_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]