# Generated by Django 5.0.6 on 2024-05-30 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_is_view'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('view_all_clients', 'can view all clients'), ('set_active', 'can activate clients')], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_view',
        ),
    ]
