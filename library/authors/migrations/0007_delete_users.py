# Generated by Django 3.2.8 on 2023-02-26 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0006_test'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Users',
        ),
    ]