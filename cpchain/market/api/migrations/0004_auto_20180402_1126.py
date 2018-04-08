# Generated by Django 2.0.3 on 2018-04-02 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20180330_1553'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='verify_code',
            new_name='signature',
        ),
        migrations.AddField(
            model_name='product',
            name='file_md5',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.IntegerField(default=0, verbose_name='0:normal,1:frozen'),
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.CharField(max_length=200, null=True),
        ),
    ]