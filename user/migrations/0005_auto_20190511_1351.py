# Generated by Django 2.2.1 on 2019-05-11 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_current_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='current_location',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.Location'),
        ),
    ]
