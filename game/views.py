from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.forms import formset_factory

def InitializeGameView(request):
    PlayerFormSet = formset_factory(PlayerForm, extra=4)
    if request.method == 'POST':
        formset = PlayerFormSet(request.POST)
        if formset.is_valid():
            game = Game()
            game.save(formset=formset)
            return redirect("game", pk=game.id)
    else:
        formset = PlayerFormSet()

    return render(request, 'game/game_create.html',
           {'formset': formset})

class GameListView(ListView):
    model = Game
    queryset = Game.objects.filter(is_active=True)

class HistoryGameListView(ListView):
    model = Game
    queryset = Game.objects.filter(is_active=False)

class GameDeleteView(DeleteView):
    model = Game
    def get_success_url(self):
        game = self.object
        if game.is_active:
            return reverse_lazy('game_list')
        else:
            return reverse_lazy('history_list')

def GameView(request, pk):
    RoundFormSet = formset_factory(RoundForm, extra=0)
    game = get_object_or_404(Game, id=pk)
    rounds = game.rounds.all()
    is_active = game.is_active
    if not is_active:
        return render(request, 'game/game.html',
                      {'is_active': is_active,
                       'game': game,
                       'rounds': rounds})
    if request.method == 'POST':
        formset = RoundFormSet(request.POST)
        if formset.is_valid():
            winner = int(request.POST['winner'])
            game.save(winner=winner, formset=formset)
    else:
        formset = RoundFormSet(initial=[{
            'unmultiplied_round_score': 0,
            'multiplicator': 1
        } for _ in range(4)])
    return render(request, 'game/game.html',
                  {'formset': formset,
                   'is_active': is_active,
                   'game': game,
                   'rounds': rounds})