# Generated by Django 4.2.5 on 2023-10-06 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('management', '0001_initial'),
        ('testing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='testing.subject'),
        ),
    ]
