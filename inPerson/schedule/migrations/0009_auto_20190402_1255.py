# Generated by Django 2.1.7 on 2019-04-02 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0008_auto_20190402_1253'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='semester',
            new_name='term',
        ),
    ]