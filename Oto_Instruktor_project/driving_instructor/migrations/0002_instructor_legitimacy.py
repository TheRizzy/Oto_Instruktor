# Generated by Django 4.2.3 on 2023-07-29 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driving_instructor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='legitimacy',
            field=models.ImageField(blank=True, null=True, upload_to='legitimacy/'),
        ),
    ]
