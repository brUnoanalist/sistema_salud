# Generated by Django 5.1.2 on 2024-11-04 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('usuarios', '0006_customuser_ciudad_customuser_comuna'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={},
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['ciudad'], name='usuarios_cu_ciudad_4610f7_idx'),
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['comuna'], name='usuarios_cu_comuna_386c97_idx'),
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['specialties'], name='usuarios_cu_special_dce22d_idx'),
        ),
    ]