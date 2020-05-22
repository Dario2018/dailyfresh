# Generated by Django 2.2.5 on 2019-09-08 16:57

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=20, verbose_name='分类名称')),
                ('logo', models.CharField(max_length=10, verbose_name='标识')),
                ('image', models.ImageField(upload_to='category', verbose_name='商品类型图片')),
            ],
            options={
                'verbose_name': '商品分类',
                'verbose_name_plural': '商品分类',
                'db_table': 'product_category',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='商品SPU名称')),
                ('detail', tinymce.models.HTMLField(blank=True, verbose_name='商品详情')),
            ],
            options={
                'verbose_name': '商品SPU',
                'verbose_name_plural': '商品SPU',
                'db_table': 'products',
            },
        ),
    ]