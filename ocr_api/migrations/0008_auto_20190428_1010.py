# Generated by Django 2.1.7 on 2019-04-28 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr_api', '0007_auto_20190426_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwordhistory',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
