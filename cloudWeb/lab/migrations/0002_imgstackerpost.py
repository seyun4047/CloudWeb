# Generated by Django 5.0.2 on 2024-02-25 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImgStackerPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, upload_to='lab/ImgStacker/images')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
