import csv
import datetime
import io
from .simplestats import mean, pstdev
from PlayersManagement.models import Player
from gamescoring.models import GameNumber,Participant
from gamescoring.backend import ranking

def main():
    WriteTables('501')

def WriteTables(tabletype):
    qgames = GameNumber.objects.filter(category=tabletype)
    maxp = 0
    tranks = []
    ranktable = {}
    tottable = {}
    for game in qgames:
        players = game.participant_set.all()
        #get the max number of players
        nplayers = len(players)
        if nplayers > maxp:
            maxp = nplayers
        ranks = {}
        for player in players:
            ranks[str(player.player)] = player.rank
            # build the summary_table
            if str(player.player) in ranktable:
                ranktable[str(player.player)].append(player.rank)
                tottable[str(player.player)] += nplayers + 1 - player.rank
            else:
                ranktable[str(player.player)] = [player.rank]
                tottable[str(player.player)] = nplayers+1-player.rank
        tranks.append([game.gamenumber, game.date.strftime("%Y-%m-%d"), game.time.strftime("%H:%M")] + _ranking(ranks, maxp))
    st = _summary_table(ranktable, tottable, maxp)
    maxplist = [str(i) for i in range(1, maxp + 1)]
    headerrank = ['#', 'Date', 'Time'] + maxplist
    headersummary = [' '] + maxplist + ['pts']
    return (tranks,st, headerrank, headersummary,maxplist)

def WriteScoreTables():
    qgames = GameNumber.objects.filter(category='BB')
    maxp=0
    tbb = []

    # check for all players in qgames
    # is there a more efficient way of doing that?
    temp_psets = []
    for game in qgames:
        players = game.participant_set.all()
        temp_psets= temp_psets + [str(p.player) for p in players]

    allplayers = list(set(temp_psets))

    for game in qgames:
        players = game.participant_set.all()
        nplayers = len(players)
        if nplayers > maxp:
            maxp = nplayers
        totscore = 0
        scores = {}
        for player in players:
            scores[str(player.player)]= player.score
            totscore += player.score

        #calculate the mean
        m = "{0:0.2f}".format(totscore/nplayers)

        tbb.append([game.gamenumber, game.date.strftime("%Y-%m-%d"), game.time.strftime("%H:%M")]+_bbranking(scores,allplayers)+[m])
    ssbb = _scoressum_table(tbb,maxp)
    #players_in_table = [p.name for p in qplayers]
    headerscore = ['#', 'Date', 'Time'] + allplayers + ['Mean']
    headersumscore = [' '] + allplayers
    return (tbb, ssbb,headerscore, headersumscore, maxp)

def _summary_table(r, t, m):
    '''
        -r is a dict with the position of the player in each game
        such as {'PP': [1, 2, 3, 2], 'HH22': [2, 1, 2, 3], 'HH18': [3, 2, 1, 1]}
        -t is a dict with the total points of all players such as
        {'PP': 9, 'HH22': 9, 'HH18': 7, 'Red': 4}
        -m is the max number of players in all the games
        This function creates a summary table and the output will be a list of list such as:
            [[PP, 	41,	31,	32,	217],
            [HH22,	37,	31,	36,	209],
            [HH18,	29,	43,	32,	205]]
    '''
    result = []
    for k in r:
        result.append([k]+ [r[k].count(i) for i in range(1,1+m)] + [t[k]])
    result.sort(key=lambda x: x[m+1], reverse=True)
    return result

def _scoressum_table(ll,m):
    '''
        ll is a list of lists from the build_table function
        This function will create a summary table with the average points
        for each player in all games.
        The output will be a list of list like:
            [[''   	PP	HH18	HH22],
             [Mean	42	42	41],
             [STDev	6.32	6.4	5.83]]
    '''
    temp = [list(_transpose(ll, 3+i)) for i in range(m)]
    result = [['Mean']+[0 for i in range(m)], ['STDev']+[0 for i in range(m)]]
    for i in range(0, m):
        cleaned_temp = list(filter(None, temp[i]))
        result[0][i + 1] = "{0:0.2f}".format(mean(cleaned_temp))
        result[1][i + 1] = "{0:0.2f}".format(pstdev(cleaned_temp))
    return result

def _transpose(ll,p):
    '''
        This function will transpose the elements of a peculiar position
        in a list of lists
        ll is a list of lists
        p is the position to be transpose
        [[1,2,3],[1,2,3]] -> [1,1] or [2,2] or [3,3] according to p
    '''
    for l in ll:
        yield l[p]

def _ranking(d, m):
    """
    Format the rank columns in the following style according to the
    selected rank for each player and return a dictionary
    PP	        HH22	HH18
    PP+HH18		      HH22
    m is the max number of players in all the games
    """
    return ['+'.join(p for p in d if d[p] == k) for k in range(1, m + 1)]

def _bbranking(scores, players):
    """
    Format the rank columns in the following style according to the
    selected rank for each player and return a dictionary
    PP	        HH22	HH18
    PP+HH18		      HH22
    m is the max number of players in all the games
    """
    result = [None for i in range(len(players))]
    for s in scores:
        result[players.index(s)]=scores[s]
    return result

def Write_csv(h1, l1, h2, l2):
    """
    write a csv file
        o = output file name
        h1-2 is a list with the table columns header
        l1-2 is a list of list of elements to display in the table
    """
    #
    # create csv in memory as StringIO
    #
    mem_file = io.StringIO()
    csv_writer = csv.writer(mem_file)
    csv_writer.writerow(h1)
    csv_writer.writerows(l1)
    csv_writer.writerows([''])
    csv_writer.writerow(h2)
    csv_writer.writerows(l2)
    csv_writer.writerows([''])
    mem_file.seek(0)
    return mem_file

def CSV_to_db(f):
    """
    Import previous data from a csv file to the db
    format should be:   501	114	2018-01-07	23:52	2	3	1
                        BB	     1	2016-03-04	23:34	46	47	42
    the three last columns contains the score/rank of PP HH22 and HH18
    """

    file_data = f.read().decode("utf-8")

    lines = file_data.split("\n")
    # loop over the lines and save them in db. If error , store as string and then display
    players = Player.objects.filter(active=True)
    for line in lines:
        fields = line.split(",")
        if len(fields) > 1:
            g = GameNumber(date=datetime.datetime.strptime(fields[2], "%Y-%m-%d").date(),
                           time=datetime.datetime.strptime(fields[3], "%H:%M").time(),
                           gamenumber= fields[1],
                           category=fields[0])
            g.save()
            pscore = [fields[4+i] for i in range(0,3)]
            if fields[0] == 'BB':
                pranks = ranking(pscore)
            else:
                pranks = list(pscore)
                pscore = [None for i in range(len(pscore))]
            i = 0
            for p in players:
                s = Participant(game=g, rank=pranks[i], score=pscore[i],  player=p)
                s.save()
                i += 1

if __name__ == "__main__":
    main()
