# Generated by Django 4.2.6 on 2024-01-19 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPApp', '0002_rename_family_chat_family_rename_family_user_family_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image_url',
            field=models.CharField(default='https://raspimartin.amor/pp-backend/raw/e94a5943a7335d75615875e112f1387a5ae6c814/PPAPI/PPApp/los_pinguinos.jpg', max_length=500),
        ),
    ]
