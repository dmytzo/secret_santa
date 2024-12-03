from django import forms

from hohoho.models import SecretSanta, UserSecretSantaGame, Rules


class SecretSantaForm(forms.ModelForm):

    class Meta:
        fields = ['name', 'budget']
        model = SecretSanta


class RuleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        game = kwargs.pop('game', None)
        super().__init__(*args, **kwargs)

        queryset = game.user_game.all()
        self.fields['player1'] = forms.ModelChoiceField(required=True, label="Player 1",
                                                        queryset=queryset,
                                                        widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['player2'] = forms.ModelChoiceField(required=True, label="Player 2",
                                                        queryset=queryset,
                                                        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        fields = ['player1', 'player2']
        model = Rules

    def clean(self):
        cd = self.cleaned_data

        if cd.get('player1') == cd.get('player2'):
            self.add_error('player2', "Can not be the same person :(")
        return cd


class CodeForm(forms.Form):

    code = forms.CharField(required=True, max_length=15)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cd = self.cleaned_data
        game = SecretSanta.objects.filter(code=cd.get('code')).first()
        if not game:
            self.add_error('code', "Wrong code :(")
        else:
            user_game = self.user.games.filter(game=game).first()
            if user_game:
                self.add_error('code', "Already exist :(")
        return cd


class UserSecretSantaGameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # game = kwargs.pop('game', None)
        # instance = kwargs.get('instance', None)
        # queryset = (game.players.filter(user_player__isnull=True) if not instance
        #             else game.players.filter(id=instance.player.id))
        super().__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(required=True, label="Your name",
                                              widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['wish'] = forms.CharField(required=False, label="Your wish",
                                              widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        fields = ['name', 'wish']
        model = UserSecretSantaGame
