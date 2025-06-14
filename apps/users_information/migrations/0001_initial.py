# Generated by Django 5.2.1 on 2025-05-28 06:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('country', models.CharField(max_length=100)),
                ('preferred_study_country', models.CharField(blank=True, max_length=100)),
                ('current_degree', models.CharField(max_length=100)),
                ('field_of_study', models.CharField(max_length=100)),
                ('gpa', models.DecimalField(decimal_places=2, max_digits=4)),
                ('gre_score', models.PositiveIntegerField(blank=True, null=True)),
                ('ielts_score', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('toefl_score', models.PositiveIntegerField(blank=True, null=True)),
                ('cgpa_scale', models.DecimalField(decimal_places=1, default=4.0, max_digits=3)),
                ('has_research_experience', models.BooleanField(default=False)),
                ('research_area', models.CharField(blank=True, max_length=255)),
                ('number_of_publications', models.PositiveIntegerField(default=0)),
                ('work_experience_years', models.DecimalField(decimal_places=1, default=0.0, max_digits=4)),
                ('cv_file', models.FileField(blank=True, null=True, upload_to='cv_uploads/')),
                ('interested_degree', models.CharField(blank=True, max_length=100)),
                ('preferred_university_type', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('custom_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
