# Generated by Django 4.2.4 on 2023-10-31 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discountcode',
            name='percent',
        ),
        migrations.AddField(
            model_name='discountcode',
            name='type',
            field=models.TextField(choices=[('PERCENT', 'Percent'), ('RIAL', 'Rial')], default='PERCENT'),
        ),
        migrations.AddField(
            model_name='discountcode',
            name='value',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
