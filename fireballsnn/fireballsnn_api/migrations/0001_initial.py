# Generated by Django 4.2.7 on 2023-12-02 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourtName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case', models.CharField(default='', max_length=16)),
                ('value', models.CharField(default='', max_length=200)),
            ],
        ),
    ]
