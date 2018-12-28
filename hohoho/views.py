from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, FormView, DeleteView
from django.views.generic.base import View

from hohoho.forms import SecretSantaForm, CodeForm, UserSecretSantaGameForm, RuleForm
from hohoho.models import SecretSanta, UserSecretSantaGame, Rules


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration.html', {'form': form})


@method_decorator(login_required(login_url='login/'), name='dispatch')
class MainView(FormView):
    template_name = 'main_page.html'
    form_class = CodeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        game = SecretSanta.objects.get(code=self.request.POST['code'])
        return redirect('join-game', game.id)


@method_decorator(login_required(login_url='login/'), name='dispatch')
class NewGameView(CreateView):
    template_name = 'newgame.html'
    form_class = SecretSantaForm
    model = SecretSanta

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_add = self.request.user
        self.object.save()
        UserSecretSantaGame.objects.create(game=self.object, user=self.request.user,
                                           name=self.request.POST['your_name'],
                                           wish=self.request.POST['wish'])
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('game', args=[self.object.id])


@method_decorator(login_required(login_url='login/'), name='dispatch')
class GameView(FormView):
    template_name = 'game.html'
    form_class = RuleForm
    model = Rules

    def get_context_data(self, **kwargs):
        game = SecretSanta.objects.get(pk=self.kwargs.get('game_pk'))
        context = super().get_context_data(**kwargs)
        context.update({
            'game': game,
            'user_game': game.user_game.filter(user=self.request.user).first(),
        })
        return context

    def form_valid(self, form):
        self.game = SecretSanta.objects.get(pk=self.kwargs.get('game_pk'))
        rule = form.save(commit=False)
        rule.game = self.game
        rule.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('game', args=[self.game.id])

    def get_form_kwargs(self):
        game = SecretSanta.objects.get(pk=self.kwargs['game_pk'])
        kwargs = super().get_form_kwargs()
        kwargs.update({'game': game})
        return kwargs


@method_decorator(login_required(login_url='login/'), name='dispatch')
class GenerateView(View):
    def get(self, request, *args, **kwargs):
        game = SecretSanta.objects.get(pk=self.kwargs['game_pk'])
        user_game = self.request.user.games.filter(game=game).first()

        gift_to_players = [i for i in game.user_game.values_list('gift_to_player', flat=True) if i]
        rules_player1 = [i.player2.id for i in game.game_rules.filter(player1=user_game)]
        rules_player2 = [i.player1.id for i in game.game_rules.filter(player2=user_game)]

        not_available_player = set(gift_to_players + rules_player1 + rules_player2 + [user_game.id])
        player = game.user_game.exclude(id__in=not_available_player).order_by('?').first()
        print(player)
        user_game.gift_to_player = player
        user_game.save()
        return redirect('game', kwargs['game_pk'])


@method_decorator(login_required(login_url='login/'), name='dispatch')
class StartGameView(View):
    def get(self, request, *args, **kwargs):
        game = SecretSanta.objects.get(pk=self.kwargs['game_pk'])
        game.ready = True
        game.save()
        return redirect('game', kwargs['game_pk'])


@method_decorator(login_required(login_url='login/'), name='dispatch')
class JoinGameView(FormView):
    template_name = 'join_game.html'
    model = UserSecretSantaGame
    form_class = UserSecretSantaGameForm

    def get_form_kwargs(self):
        game = SecretSanta.objects.get(pk=self.kwargs['game_pk'])
        kwargs = super().get_form_kwargs()
        user_game = self.request.user.games.filter(game=game).first()
        if user_game:
            kwargs.update({'instance': user_game})
        return kwargs

    def get_context_data(self, **kwargs):
        game = SecretSanta.objects.get(pk=self.kwargs['game_pk'])
        context = super().get_context_data(**kwargs)
        context.update({
            'instance': self.request.user.games.filter(game=game).first(),
        })
        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        object.game_id = self.kwargs['game_pk']
        object.user = self.request.user
        object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('game', args=[self.kwargs['game_pk']])


@method_decorator(login_required(login_url='login/'), name='dispatch')
class DeleteGameView(DeleteView):
    model = UserSecretSantaGame
    pk_url_kwarg = 'user_game_pk'
    success_url = reverse_lazy('main')
    template_name = 'usersecretsantagame_confirm_delete.html'



