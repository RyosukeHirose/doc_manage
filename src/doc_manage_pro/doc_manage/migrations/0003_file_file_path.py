# Generated by Django 2.2.10 on 2020-06-13 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doc_manage', '0002_auto_20200613_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file_path',
            field=models.CharField(default='', max_length=255),
        ),
    ]
