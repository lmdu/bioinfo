# Generated by Django 2.0 on 2018-05-06 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('big', '0002_publication_doi'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='abstract',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
