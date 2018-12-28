import random
import string

from django.contrib.auth import get_user_model
from django.db import models


def generate_code():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(15))


class SecretSanta(models.Model):
    name = models.CharField(max_length=200)
    budget = models.CharField(max_length=200)
    code = models.CharField(max_length=15, default=generate_code)
    user_add = models.ForeignKey(get_user_model(), related_name='own_games', on_delete=models.CASCADE, null=True)
    ready = models.BooleanField(default=False)


class UserSecretSantaGame(models.Model):
    game = models.ForeignKey(SecretSanta, related_name='user_game', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(get_user_model(), related_name='games', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    wish = models.CharField(max_length=2000)
    gift_to_player = models.ForeignKey('self', related_name='gift_users', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Rules(models.Model):
    game = models.ForeignKey(SecretSanta, related_name='game_rules', on_delete=models.CASCADE, null=True)
    player1 = models.ForeignKey(UserSecretSantaGame, related_name='player1_in_rule', on_delete=models.CASCADE,
                                null=True)
    player2 = models.ForeignKey(UserSecretSantaGame, related_name='player2_in_rule', on_delete=models.CASCADE,
                                null=True)

    def __str__(self):
        return f'Players: {self.player1} and {self.player2} can not be together!'
