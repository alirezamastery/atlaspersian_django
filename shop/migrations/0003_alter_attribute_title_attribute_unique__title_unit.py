# Generated by Django 4.2.4 on 2023-11-02 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_remove_discountcode_percent_discountcode_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AddConstraint(
            model_name='attribute',
            constraint=models.UniqueConstraint(fields=('title', 'unit'), name='unique__title_unit'),
        ),
    ]
