# Generated by Django 2.1.2 on 2018-11-04 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20181103_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tweet_created',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]