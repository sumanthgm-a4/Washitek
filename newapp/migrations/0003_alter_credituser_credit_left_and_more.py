# Generated by Django 5.0.7 on 2024-09-09 08:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("newapp", "0002_item_credituser_payperpieceuser_yearlyuser"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="credituser",
            name="credit_left",
            field=models.FloatField(default=500),
        ),
        migrations.AlterField(
            model_name="yearlyuser",
            name="amt_left",
            field=models.FloatField(default=10000),
        ),
        migrations.CreateModel(
            name="Order",
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
                ("orderdate", models.DateField(auto_now_add=True)),
                ("quantity", models.IntegerField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("RECEIVED", "RECEIVED"),
                            ("PROCESSING", "PROCESSING"),
                            ("READY TO DELIVER", "READY TO DELIVER"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "itemobj",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="newapp.item"
                    ),
                ),
                (
                    "userobj",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="PayPerPieceUser",
        ),
    ]