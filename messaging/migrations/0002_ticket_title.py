# Generated by Django 3.2.5 on 2021-07-27 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='title',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]
