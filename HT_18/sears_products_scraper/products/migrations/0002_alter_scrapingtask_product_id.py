# Generated by Django 5.0 on 2023-12-29 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrapingtask',
            name='product_id',
            field=models.CharField(max_length=255),
        ),
    ]
