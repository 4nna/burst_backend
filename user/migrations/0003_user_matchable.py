# Generated by Django 2.2.1 on 2019-05-11 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20190511_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='matchable',
            field=models.BooleanField(default=False),
        ),
    ]