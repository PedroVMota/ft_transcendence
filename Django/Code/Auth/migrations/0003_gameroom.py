# Generated by Django 4.2.13 on 2024-09-14 18:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0002_myuser_walletcoins'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameRoom',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('GameName', models.CharField(max_length=255)),
                ('GameStates', models.IntegerField(choices=[(1, 'In Progress'), (2, 'Not Started'), (3, 'Completed')], default=2)),
                ('GameChat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Auth.currentchat')),
                ('PlayerOne', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_one_games', to=settings.AUTH_USER_MODEL)),
                ('PlayerTwo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_two_games', to=settings.AUTH_USER_MODEL)),
                ('Spectators', models.ManyToManyField(blank=True, related_name='spectated_games', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
