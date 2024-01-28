# Generated by Django 5.0 on 2024-01-16 20:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_scrapingtask_product_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='scrapedproduct',
            name='category_name',
        ),
        migrations.AddField(
            model_name='scrapedproduct',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='products.category'),
        ),
    ]