# Generated by Django 5.1.1 on 2024-09-19 12:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_customuser_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='class_assigned',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='core.class'),
        ),
    ]
