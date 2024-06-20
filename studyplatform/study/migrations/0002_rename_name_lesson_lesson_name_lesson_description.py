# Generated by Django 5.0.6 on 2024-06-20 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='name',
            new_name='lesson_name',
        ),
        migrations.AddField(
            model_name='lesson',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]