# Generated by Django 3.2.6 on 2021-08-03 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_email', models.CharField(max_length=200)),
                ('to_name', models.CharField(max_length=100)),
                ('from_email', models.CharField(max_length=200)),
                ('from_name', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=500)),
                ('body', models.TextField()),
                ('status', models.CharField(blank=True, max_length=10, null=True)),
                ('sent_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]