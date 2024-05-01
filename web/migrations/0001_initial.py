# Generated by Django 5.0.2 on 2024-04-23 15:38

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('nationality', models.CharField(max_length=100)),
                ('monthly_listeners', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('artists', models.ManyToManyField(related_name='artists_to_genre', to='web.artist')),
            ],
        ),
        migrations.AddField(
            model_name='artist',
            name='genres',
            field=models.ManyToManyField(related_name='genres_to_artist', to='web.genre'),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('album', models.CharField(max_length=100)),
                ('duration', models.DurationField()),
                ('lyrics', models.TextField()),
                ('artists', models.ManyToManyField(related_name='artists_to_song', to='web.artist')),
                ('genre', models.ManyToManyField(related_name='genres_to_song', to='web.genre')),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField(default=datetime.date.today)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('songs', models.ManyToManyField(related_name='songs_to_playlist', to='web.song')),
            ],
        ),
        migrations.AddField(
            model_name='genre',
            name='songs',
            field=models.ManyToManyField(related_name='songs_to_genre', to='web.song'),
        ),
        migrations.AddField(
            model_name='artist',
            name='songs',
            field=models.ManyToManyField(related_name='songs_to_artist', to='web.song'),
        ),
    ]
