# Generated by Django 4.1.4 on 2022-12-29 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_surveys', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='date_start',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата старта'),
        ),
    ]