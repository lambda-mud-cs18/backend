# Generated by Django 2.2.3 on 2019-07-31 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('weight', models.IntegerField()),
                ('itemtype', models.CharField(max_length=200)),
                ('level', models.IntegerField()),
                ('exp', models.IntegerField()),
                ('attributes', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('playername', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('team_id', models.IntegerField()),
                ('current_room', models.IntegerField()),
                ('cooldown', models.FloatField()),
                ('encumbrance', models.IntegerField()),
                ('strength', models.IntegerField()),
                ('speed', models.IntegerField()),
                ('gold', models.IntegerField()),
                ('inventory', models.CharField(max_length=1000)),
                ('status', models.CharField(max_length=1000)),
                ('errors', models.CharField(max_length=1000)),
                ('messages', models.CharField(max_length=1000)),
                ('token', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerInventory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('player_id', models.IntegerField()),
                ('item_id', models.IntegerField()),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('map_id', models.IntegerField()),
                ('room_id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('coordinates', models.CharField(max_length=200)),
                ('elevation', models.IntegerField()),
                ('terrain', models.CharField(max_length=200)),
                ('north', models.CharField(max_length=200)),
                ('south', models.CharField(max_length=200)),
                ('east', models.CharField(max_length=200)),
                ('west', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('map_id', models.IntegerField()),
            ],
        ),
    ]
