from django.db import models

PLAYER_NUMBERS = (
                    (1,1),
                    (2,2),
                    (3,3),
                    (4,4),
)

class Player(models.Model):
    order = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    game = models.ForeignKey('Game', related_name='players',
                             on_delete=models.CASCADE,
                             null=True, blank=True)
    current_score = models.IntegerField(default=0)
    unmultiplied_round_score = models.IntegerField(default=0)
    multiplicator = models.IntegerField(default=1)
    raw_round_score = models.IntegerField(default=0)
    actual_round_score = models.IntegerField(default=0)

    def CalculateCurrentScore(self):
        order = self.order
        raw_round_score = self.raw_round_score
        east_order = self.game.east
        winner_order = self.game.winner
        raw_scores = [player.raw_round_score for
                      player in self.game.players.all()]
        if order == winner_order:
            score = 3 * raw_round_score
            if order == east_order:
                score *= 2
            else:
                score += raw_round_score
        else:
            score = 3*raw_round_score - sum(raw_scores)
            if order == east_order:
                score *= 2
            else:
                if winner_order == east_order:
                    score -= raw_scores[east_order-1]
                else:
                    score += raw_round_score\
                             - raw_scores[east_order-1]
        self.actual_round_score = score
        self.current_score += score
        self.save()

    def save(self, *args, **kwargs):
        if 'CRRS' in kwargs:
            kwargs.pop('CRRS')
            self.raw_round_score = self.multiplicator\
                                   * self.unmultiplied_round_score
        super(Player, self).save(*args, **kwargs)

    def __str__(self):
        _sign = ""
        if self.actual_round_score>0:
            _sign = "+"
        return f'{self.name}: {self.current_score} ({_sign}' \
               f'{self.actual_round_score})'

class Game(models.Model):
    east = models.IntegerField(default=0)
    winner = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def SwitchEast(self):
        if self.east != self.winner:
            self.east += 1
            if self.east >= 5:
                self.is_active = False
        self.save()

    def NewWinner(self, winner):
        self.winner = winner
        self.save()

    def save(self, *args, **kwargs):
        if 'winner' in kwargs:
            winner = kwargs.pop('winner')
            self.NewWinner(winner)
            formset = kwargs.pop('formset')
            for player in self.players.all():
                for i, form in enumerate(formset):
                    player = self.players.all().get(order=i+1)
                    cd = form.cleaned_data
                    player.unmultiplied_round_score = \
                        cd['unmultiplied_round_score']
                    player.multiplicator = \
                        cd['multiplicator']
                    player.save(CRRS=True)
            for player in self.players.all():
                player.CalculateCurrentScore()

            round = Round.objects.create(game=self)
            round_lst =[str(player) for player in self.players.all()]
            round_lst[self.east-1] += " (e)"
            round.CalculateResult(*round_lst)
            self.SwitchEast()
            super(Game, self).save(*args, **kwargs)

        elif 'formset' in kwargs:
            self.east = 1
            formset = kwargs.pop('formset')
            super(Game, self).save(*args, **kwargs)
            for i, form in enumerate(formset):
                player = form.save(commit=False)
                player.game = self
                player.order = i+1
                player.save()

        else:
            super(Game, self).save(*args, **kwargs)

    def __str__(self):
        st = ""
        for player in self.players.all():
            st += str(player) + "\n"
        return st

class Round(models.Model):
    game = models.ForeignKey(Game, related_name='rounds',
                             on_delete=models.CASCADE)
    result = models.CharField(max_length=256, null=True)

    def CalculateResult(self, *args):
        self.result = '\n'.join(args)
        self.save()

    def __str__(self):
        return self.result