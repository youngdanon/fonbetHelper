# Generated by Django 3.2.9 on 2021-11-20 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_eventsegment_factors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventsegment',
            name='factors',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.factor'),
        ),
    ]