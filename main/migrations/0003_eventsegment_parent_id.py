# Generated by Django 3.2.9 on 2021-11-21 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20211121_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventsegment',
            name='parent_id',
            field=models.IntegerField(default=-1, verbose_name='parent_id'),
        ),
    ]
