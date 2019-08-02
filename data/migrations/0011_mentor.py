# Generated by Django 2.1.7 on 2019-08-02 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0010_unassignedissuesactivity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('year', models.SmallIntegerField(verbose_name='Mentoring year')),
                ('program', models.CharField(max_length=20, verbose_name='Mentoring program')),
            ],
        ),
    ]
