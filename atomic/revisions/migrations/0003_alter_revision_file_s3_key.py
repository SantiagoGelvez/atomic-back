# Generated by Django 5.1.1 on 2024-09-17 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('revisions', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revision',
            name='file_s3_key',
            field=models.FileField(upload_to='revisions/'),
        ),
    ]
