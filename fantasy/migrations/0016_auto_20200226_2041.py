# Generated by Django 2.2.4 on 2020-02-26 20:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0015_auto_20200226_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fantasyclub',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
