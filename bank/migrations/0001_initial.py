# Generated by Django 5.0.6 on 2024-06-04 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=255)),
                ('lname', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('house', models.CharField(max_length=255)),
                ('image', models.ImageField(null=True, upload_to='customerImages')),
            ],
        ),
    ]