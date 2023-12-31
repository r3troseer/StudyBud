# Generated by Django 4.2.2 on 2023-08-06 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_summary'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='summary',
            options={'verbose_name_plural': 'summaries'},
        ),
        migrations.RenameField(
            model_name='summary',
            old_name='text',
            new_name='document',
        ),
        migrations.AddField(
            model_name='summary',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
