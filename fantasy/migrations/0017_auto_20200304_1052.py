# Generated by Django 3.0.3 on 2020-03-04 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0016_auto_20200226_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
