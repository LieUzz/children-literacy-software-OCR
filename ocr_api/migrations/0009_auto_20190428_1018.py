# Generated by Django 2.1.7 on 2019-04-28 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr_api', '0008_auto_20190428_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwordhistory',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
