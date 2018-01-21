from django.db import models
from PlayersManagement.models import Player

GAMETYPE_CHOICES = (
    ('BB', 'Baseball'),
    ('501', '501'),
)

class GameNumber(models.Model):
    gamenumber  = models.IntegerField(null=True)
    date        = models.DateField()
    time        = models.TimeField()
    category    = models.CharField(choices=GAMETYPE_CHOICES,max_length = 10)
    def __str__(self):
        return "{0}-{1}".format(self.date, self.time)

class Participant(models.Model):
    score       = models.IntegerField(null=True,blank=True)
    rank        = models.IntegerField()
    player      = models.ForeignKey(Player, on_delete = models.CASCADE)
    game        = models.ForeignKey(GameNumber, on_delete = models.CASCADE)
    def __str__(self):
        return "{0}({1}):{2}-{3}-{4}".format(self.game.category, self.game.gamenumber, self.player, self.score, self.rank)

