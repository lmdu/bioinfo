# Generated by Django 2.0 on 2018-05-13 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('big', '0002_auto_20180510_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='thumbnail',
            field=models.ImageField(default='', upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='thumbnail',
            field=models.ImageField(default='', upload_to=''),
            preserve_default=False,
        ),
    ]
