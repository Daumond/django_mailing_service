# Generated by Django 5.0.6 on 2024-05-30 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_view',
            field=models.BooleanField(default=False, verbose_name='признак просмотра'),
        ),
    ]