# Generated by Django 2.0 on 2018-06-07 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': '评论记录', 'verbose_name_plural': '评论记录'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='object_id',
            field=models.PositiveSmallIntegerField(verbose_name='关联对象'),
        ),
    ]