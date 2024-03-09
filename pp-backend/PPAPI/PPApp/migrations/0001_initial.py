# Generated by Django 4.2.6 on 2024-01-12 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family_hash', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
                ('price', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('e_mail', models.CharField(max_length=260, unique=True)),
                ('username', models.CharField(max_length=240)),
                ('encrypted_password', models.CharField(max_length=120)),
                ('user_token', models.CharField(blank=True, max_length=45, null=True, unique=True)),
                ('family', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='PPApp.family')),
            ],
        ),
        migrations.CreateModel(
            name='Shop_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_name', models.CharField(max_length=100)),
                ('family', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='PPApp.family')),
            ],
        ),
        migrations.CreateModel(
            name='ProductsinLists',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('bought', models.BooleanField(default=False)),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PPApp.shop_list')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='PPApp.products')),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('message', models.CharField(max_length=1000)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PPApp.family')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='PPApp.user')),
            ],
        ),
    ]