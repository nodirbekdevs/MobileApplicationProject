# Generated by Django 4.2.5 on 2023-10-08 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0001_initial'),
        ('management', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='testing.subject'),
        ),
    ]