# Generated by Django 5.1.1 on 2024-09-15 15:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_customuser_student_class_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentClassAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_assigned', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.class')),
                ('student', models.ForeignKey(limit_choices_to={'role': 'student'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('student', 'class_assigned')},
            },
        ),
        migrations.CreateModel(
            name='TeacherClassAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_assigned', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.class')),
                ('teacher', models.ForeignKey(limit_choices_to={'role': 'teacher'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('teacher', 'class_assigned')},
            },
        ),
    ]
