# Generated by Django 3.2.5 on 2021-07-17 15:06

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=79)),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True)),
                ('group', models.CharField(blank=True, default=None, max_length=1, null=True)),
            ],
            options={
                'db_table': 'employee',
            },
            managers=[
                ('from_bpm', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddIndex(
            model_name='employee',
            index=models.Index(fields=['group'], name='employee_group_e2baac_idx'),
        ),
    ]
