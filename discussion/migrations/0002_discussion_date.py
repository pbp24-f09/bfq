# Generated by Django 5.1.2 on 2024-10-26 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
