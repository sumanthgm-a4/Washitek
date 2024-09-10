# Generated by Django 5.0.7 on 2024-09-10 06:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "newapp",
            "0006_remove_monthlyuser_userobj_remove_yearlyuser_userobj_and_more",
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CreditUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("credit_left", models.FloatField(default=500)),
                ("datetime", models.DateTimeField(auto_now_add=True)),
                ("isActive", models.BooleanField()),
                (
                    "userobj",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MonthlyUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amt_left", models.FloatField(default=3000)),
                ("datetime", models.DateTimeField(auto_now_add=True)),
                ("comf_dettol", models.BooleanField()),
                ("isActive", models.BooleanField()),
                (
                    "userobj",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="YearlyUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amt_left", models.FloatField(default=10000)),
                ("datetime", models.DateTimeField(auto_now_add=True)),
                ("comf_dettol", models.BooleanField()),
                ("isActive", models.BooleanField()),
                (
                    "userobj",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]