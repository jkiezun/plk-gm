# Generated by Django 2.2.4 on 2019-10-15 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0010_remove_player_stat_fantasy_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='player_stat',
            name='fantasy_points',
            field=models.IntegerField(default=0, editable=False),
            preserve_default=False,
        ),
    ]
