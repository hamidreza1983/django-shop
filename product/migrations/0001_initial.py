# Generated by Django 5.1.8 on 2025-04-04 14:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guarantee',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('mounts', models.PositiveBigIntegerField(default=0)),
                ('price_increase', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ProductsColor',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=100)),
                ('hex_code', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=100, unique=True)),
                (
                    'image',
                    models.ImageField(
                        default='category.png', upload_to='category_images'
                    ),
                ),
                (
                    'parent',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='subcategories',
                        to='product.category',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=255)),
                (
                    'category',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='product.category',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='ProductComment',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('email', models.EmailField(max_length=254)),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                (
                    'name',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='accounts.profile',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='ProductReplay',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('email', models.EmailField(max_length=254)),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                (
                    'comment',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='replays',
                        to='product.productcomment',
                    ),
                ),
                (
                    'name',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='accounts.profile',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('description', models.TextField()),
                ('review', models.TextField(default='نقد بلند محصول')),
                ('has_discount', models.BooleanField(default=False)),
                ('discount_price', models.PositiveBigIntegerField(default=0)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('available', models.BooleanField(default=True)),
                ('price', models.PositiveBigIntegerField()),
                (
                    'image',
                    models.ImageField(
                        default='product1.jpg', upload_to='products/'
                    ),
                ),
                (
                    'image2',
                    models.ImageField(
                        default='product2.jpg', upload_to='products/'
                    ),
                ),
                (
                    'image3',
                    models.ImageField(
                        default='product3.jpg', upload_to='products/'
                    ),
                ),
                (
                    'image4',
                    models.ImageField(
                        default='product4.jpg', upload_to='products/'
                    ),
                ),
                ('total_sold', models.PositiveIntegerField(default=0)),
                ('total_views', models.PositiveIntegerField(default=0)),
                ('total_favorites', models.PositiveIntegerField(default=0)),
                ('total_vots', models.PositiveIntegerField(default=0)),
                ('has_guarantee', models.BooleanField(default=False)),
                ('has_colored', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                (
                    'category',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='product.category',
                    ),
                ),
                (
                    'guarantees',
                    models.ManyToManyField(
                        blank=True, to='product.guarantee'
                    ),
                ),
                (
                    'color',
                    models.ManyToManyField(
                        blank=True, to='product.productscolor'
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name='productcomment',
            name='product',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='comments',
                to='product.products',
            ),
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('value', models.CharField(max_length=255)),
                (
                    'attribute',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='product.attribute',
                    ),
                ),
                (
                    'product',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='specifications',
                        to='product.products',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Faviorites',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'name',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='accounts.profile',
                    ),
                ),
                (
                    'product',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='product.products',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Compare',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'name',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='accounts.profile',
                    ),
                ),
                (
                    'product',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='product.products',
                    ),
                ),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductScore',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('score', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                (
                    'name',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='accounts.profile',
                    ),
                ),
                (
                    'product',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='scores',
                        to='product.products',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='SpecialOffer',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                (
                    'product',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='product.products',
                    ),
                ),
            ],
        ),
    ]
