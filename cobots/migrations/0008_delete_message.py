# Generated by Django 5.0.3 on 2024-03-11 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cobots', '0007_cobots_user_chat_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]