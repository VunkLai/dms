# Generated by Django 3.2.5 on 2021-07-24 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_employee_employee_name_7aabaa_idx'),
        ('hr', '0002_auto_20210724_1927'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthDeclaration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('working_from', models.CharField(max_length=16)),
                ('symptom', models.CharField(default=None, max_length=119, null=True)),
                ('measuring_type', models.CharField(max_length=30)),
                ('temperature', models.FloatField()),
                ('risk', models.CharField(max_length=30)),
                ('row61', models.TextField(default=None, null=True)),
                ('row62', models.TextField(default=None, null=True)),
                ('row63', models.TextField(default=None, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee')),
            ],
            options={
                'db_table': 'hr_health_declaration',
            },
        ),
        migrations.AddIndex(
            model_name='healthdeclaration',
            index=models.Index(fields=['working_from'], name='hr_health_d_working_22b0b1_idx'),
        ),
        migrations.AddIndex(
            model_name='healthdeclaration',
            index=models.Index(fields=['symptom'], name='hr_health_d_symptom_ee0fc8_idx'),
        ),
        migrations.AddIndex(
            model_name='healthdeclaration',
            index=models.Index(fields=['temperature'], name='hr_health_d_tempera_ed2ba0_idx'),
        ),
        migrations.AddIndex(
            model_name='healthdeclaration',
            index=models.Index(fields=['risk'], name='hr_health_d_risk_23d5cf_idx'),
        ),
    ]
