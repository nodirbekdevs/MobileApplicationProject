# Generated by Django 4.2.6 on 2023-10-30 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0004_statistics_checked_tests_statistics_solved_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistics',
            name='solved_time',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]