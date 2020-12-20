from django.test import TestCase
from game.models import *
from game.forms import *

class TestAlgorithm(TestCase):
    @classmethod
    def setUpTestData(cls):
        game = Game()
        game.save()
        player = []
        for i in range(4):
            player.append(Player(order=i+1, name=str(i+1),
                                 game=game))
            if i==0:
                player[i].east=True
            player[i].save()

    def test_initial_values(self):
        for i in range(4):
            if i==0:
                self.assertTrue(Player.objects.get(order=i+1).east)
            else:
                self.assertFalse(Player.objects.get(order=i+1).east)