# Generated by Django 4.2.6 on 2024-02-05 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPApp', '0005_merge_20240205_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='imageUrl',
            field=models.CharField(default='https://raw.githubusercontent.com/GaelRGuerreiro/fotosPingu/main/pinguino10.jpg', max_length=500),
        ),
    ]
