# Generated by Django 3.2.5 on 2021-08-01 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0003_auto_20210801_2320'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=79)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='centers', to='employee.employee')),
            ],
            options={
                'db_table': 'cost_center',
            },
        ),
    ]
