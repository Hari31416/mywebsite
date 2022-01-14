# Generated by Django 4.0.1 on 2022-01-14 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_file', models.ImageField(upload_to='images')),
                ('img_name', models.CharField(max_length=100)),
                ('img_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
