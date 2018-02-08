from django.db import models
from PlayersManagement.models import Player

from scoretable.simplestats import mean

GAMETYPE_CHOICES = (
    ('BB', 'Baseball'),
    ('501', '501'),
)

class GameNumber(models.Model):
    gamenumber  = models.IntegerField()
    date        = models.DateField()
    time        = models.TimeField()
    category    = models.CharField(choices=GAMETYPE_CHOICES,max_length = 10)
    def __str__(self):
        return "{0}-{1}".format(self.date, self.time)
    def get_all_players(self):
        return [player.player.name for player in self.participant_set.all()]
    def get_number_of_players(self):
        return len(self.get_all_players())
    def get_bb_mean(self):
        if self.category == 'BB':
            return "{0:0.2f}".format(mean([player.score for player in self.participant_set.all()]))
        else:
            return None
    def get_ranks(self):
        return {p.player.name:p.rank for p in self.participant_set.all()}
    def get_scores(self):
        return {p.player.name:p.score for p in self.participant_set.all()}
    def get_points(self):
        return {p.player.name:self.get_number_of_players() + 1 - p.rank for p in self.participant_set.all()}
    def get_ranking(self):
        """
        Format the rank columns in the following style according to the
        selected rank for each player and return a dictionary
        PP	        HH22	HH18
        PP+HH18		      HH22
        m is the max number of players in all the games
        """
        d = self.get_ranks()
        return ['+'.join(p for p in d if d[p] == k) for k in range(1, self.get_number_of_players() + 1)]


class Participant(models.Model):
    score       = models.IntegerField(null=True,blank=True)
    rank        = models.IntegerField()
    player      = models.ForeignKey(Player, on_delete = models.CASCADE)
    game        = models.ForeignKey(GameNumber, on_delete = models.CASCADE)
    def __str__(self):
        return "{0}".format(self.player)
        #return "{0}({1}):{2}-{3}-{4}".format(self.game.category, self.game.gamenumber, self.player, self.score, self.rank)

