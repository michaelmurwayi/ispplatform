# Generated by Django 3.0.7 on 2020-07-23 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccess', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Radcheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('attribute', models.CharField(max_length=64)),
                ('op', models.CharField(max_length=2)),
                ('value', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'radcheck',
                'managed': False,
            },
        ),
        migrations.RemoveField(
            model_name='selectedpackages',
            name='email',
        ),
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(default='Truth', max_length=60, unique=True),
        ),
        migrations.AddField(
            model_name='selectedpackages',
            name='bundle_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='selectedpackages',
            name='username',
            field=models.CharField(max_length=50, null=True),
        ),
    ]