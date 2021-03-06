# Generated by Django 4.0 on 2022-01-07 19:05

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookborrowed',
            name='date_borrow',
            field=models.DateField(default=datetime.date(2022, 1, 8)),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(help_text='Enter message for student...', max_length=1000)),
                ('time', models.DateTimeField(default=datetime.date(2022, 1, 8))),
                ('username', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
