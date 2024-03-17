# Generated by Django 5.0.2 on 2024-03-17 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0004_qrpost_alter_imgstackerpost_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='SongQRPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, upload_to='lab/QR/images')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
