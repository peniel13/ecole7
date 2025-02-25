# Generated by Django 5.1.1 on 2024-09-15 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_class_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='teacher',
        ),
        migrations.AddField(
            model_name='class',
            name='assigned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='assigned_classes',
            field=models.ManyToManyField(blank=True, related_name='assigned_users', to='core.class'),
        ),
    ]
