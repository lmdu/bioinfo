# Generated by Django 2.0.3 on 2018-05-10 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('big', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='publication',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='slideshow',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]