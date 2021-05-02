# Generated by Django 3.2 on 2021-05-02 14:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('title_api', '0003_auto_20210414_1852'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['name', 'year'], 'verbose_name': 'Title', 'verbose_name_plural': 'Titles'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Publication date'),
        ),
        migrations.AlterField(
            model_name='review',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Publication date'),
        ),
    ]
