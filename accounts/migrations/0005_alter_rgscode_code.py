# Generated by Django 4.0.4 on 2022-05-02 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_rgscode_code_alter_rgscode_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rgscode',
            name='code',
            field=models.IntegerField(),
        ),
    ]
