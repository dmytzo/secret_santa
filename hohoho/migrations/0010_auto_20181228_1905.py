# Generated by Django 2.1.4 on 2018-12-28 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hohoho', '0009_auto_20181228_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='rules',
            name='game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_rules', to='hohoho.SecretSanta'),
        ),
        migrations.AddField(
            model_name='secretsanta',
            name='budget',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]