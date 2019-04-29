# Generated by Django 2.1.5 on 2019-04-27 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Act',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('act_id', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=4000)),
                ('first_name', models.CharField(blank=True, max_length=10, null=True)),
                ('last_name', models.CharField(blank=True, max_length=10, null=True)),
                ('short_name', models.CharField(blank=True, max_length=8, null=True)),
                ('birthday', models.DateTimeField(blank=True, null=True)),
                ('gender', models.IntegerField(blank=True, null=True)),
                ('mail_address', models.CharField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
    ]