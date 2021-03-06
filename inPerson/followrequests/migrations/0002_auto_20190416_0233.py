# Generated by Django 2.1.7 on 2019-04-16 02:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('followrequests', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='followrequest',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_requests_sent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='followrequest',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_requests_recieved', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='followrequest',
            unique_together={('from_user', 'to_user')},
        ),
    ]
