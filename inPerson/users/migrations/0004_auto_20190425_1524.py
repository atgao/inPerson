# Generated by Django 2.1.7 on 2019-04-25 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190425_1522'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['class_year']},
        ),
    ]
