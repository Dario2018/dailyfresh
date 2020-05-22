# Generated by Django 2.2.5 on 2019-09-09 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSKU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='商品名称')),
                ('desc', models.CharField(max_length=100, verbose_name='商品简介')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品价格')),
                ('unite', models.CharField(max_length=20, verbose_name='单位')),
                ('image', models.ImageField(upload_to='products', verbose_name='商品图片')),
                ('inventory', models.IntegerField(default=0, verbose_name='库存')),
                ('sales', models.IntegerField(default=0, verbose_name='销量')),
                ('status', models.SmallIntegerField(choices=[(0, '下线'), (1, '上线'), (2, '即将上线')], default=1, verbose_name='商品状态')),
                ('create_time', models.DateTimeField(verbose_name='创建时间')),
                ('update_time', models.DateTimeField(verbose_name='更新时间')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Products', verbose_name='商品SPU')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.ProductCategory', verbose_name='所属分类')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
                'db_table': 'product_sku',
            },
        ),
        migrations.CreateModel(
            name='PromotionPc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='活动名称')),
                ('image', models.ImageField(upload_to='banner', verbose_name='活动图片')),
                ('url', models.URLField(verbose_name='互动连接')),
                ('index', models.SmallIntegerField(default=0, verbose_name='展示顺序')),
                ('start_time', models.DateTimeField(verbose_name='活动开始时间')),
                ('end_time', models.DateTimeField(verbose_name='活动结束时间')),
                ('create_time', models.DateTimeField(verbose_name='创建时间')),
                ('update_time', models.DateTimeField(verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '促销活动',
                'verbose_name_plural': '促销活动',
                'db_table': 'promotion',
            },
        ),
        migrations.CreateModel(
            name='TypeShow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_type', models.SmallIntegerField(choices=[(0, '文字'), (1, '图片')], default=1, verbose_name='展示类型')),
                ('index', models.SmallIntegerField(default=0, verbose_name='展示顺序')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.ProductSKU', verbose_name='商品SKU')),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.ProductCategory', verbose_name='商品种类')),
            ],
            options={
                'verbose_name': '分类品展示',
                'verbose_name_plural': '分类品展示',
                'db_table': 'product_show',
            },
        ),
        migrations.CreateModel(
            name='ProductBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='banner', verbose_name='轮播图片')),
                ('index', models.SmallIntegerField(default=0, verbose_name='轮播索引')),
                ('create_time', models.DateTimeField(verbose_name='创建时间')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.ProductSKU', verbose_name='商品')),
            ],
            options={
                'verbose_name': '首页轮播商品',
                'verbose_name_plural': '首页轮播商品',
                'db_table': 'product_banner',
            },
        ),
    ]