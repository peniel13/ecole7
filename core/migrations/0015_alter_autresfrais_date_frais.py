# Generated by Django 5.1.1 on 2024-09-24 11:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_convocation_delete_bloginfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autresfrais',
            name='date_frais',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
