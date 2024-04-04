import csv
import datetime
import io
from .simplestats import mean, pstdev
from playersmanagement.models import Player
from gamescoring.models import GameNumber,Participant
from gamescoring.backend import ranking


def main():
    WriteTables('501')


def WriteTables(tabletype):
    qgames = GameNumber.objects.filter(category=tabletype).order_by('-gamenumber')
    tranks = {}
    tabledict = {}
    gn = len(qgames)+1
    for game in qgames:
        gn -= 1
        ranks = game.get_ranks()
        points = game.get_points()
        for p in ranks:
            if p in tabledict:
                tabledict[p]['ranks'].append(ranks[p])
                tabledict[p]['points'] += points[p]
            else:
                tabledict[p] = {}
                tabledict[p]['ranks']= [ranks[p]]
                tabledict[p]['points'] = points[p]
        tranks[game.id] = [gn, game.date.strftime("%Y-%m-%d"), game.time.strftime("%H:%M")] + game.get_ranking()
    st = _summary_table(tabledict)
    maxplist = [str(i) for i in range(1, len(tabledict) + 1)]
    headerrank = ['#', 'Date', 'Time'] + maxplist
    headersummary = ['Name'] + maxplist + ['pts']
    return (tranks, st, headerrank, headersummary, maxplist)


def WriteScoreTables():
    qgames = GameNumber.objects.filter(category='BB').order_by('-gamenumber')
    tbb = {}
    # check for all players in qgames
    # is there a more efficient way of doing that?
    temp_psets = []
    for game in qgames:
        temp_psets= temp_psets + game.get_all_pnames()
    allplayers = list(set(temp_psets))
    maxp = len(allplayers)
    gn = len(qgames)+1
    for game in qgames:
        gn -= 1
        scores = game.get_scores()
        tbb[game.id] = [gn, game.date.strftime("%Y-%m-%d"), game.time.strftime("%H:%M")]+_bbranking(scores,allplayers)+[game.get_bb_mean()]

    ssbb = _scoressum_table(tbb,maxp,3) #2 for #, date and time
    headerscore = ['#', 'Date', 'Time'] + allplayers + ['Mean']
    headersumscore = [' '] + allplayers
    return (tbb, ssbb, headerscore, headersumscore, maxp)


def _summary_table(t):
    '''
        -t is a dict with the position (ranks) of the player in each game
        and the total points for all players such as
        {'PP': {'ranks': [2, 2, ... 2], 'points': 239},
         'HH22': {'ranks': [1, 1,... 1], 'points': 231},
          'HH18': {'ranks': [3, 3, ... 3], 'points': 222}}
        This function creates a summary table and the output will be a list of list such as:
            [[PP, 	41,	31,	32,	217],
            [HH22,	37,	31,	36,	209],
            [HH18,	29,	43,	32,	205]]
    '''
    result = []
    for k in t:
        result.append([k] + [t[k]['ranks'].count(i) for i in range(1, 1 + len(t))] + [t[k]['points']])
    result.sort(key=lambda x: x[ len(t) + 1], reverse=True)
    return result


def _scoressum_table(dict, m, n):
    '''
        dict is a dict from the build_table function
        m is the number of individuals
        n is the number of columns to skip
        This function will create a summary table with the average weigths
        for each cat in all measurements.
        The output will be a list of list like:
            [[''   	PP	HH18	HH22],
             [Mean	42	42	41],
             [STDev	6.32	6.4	5.83]]
    '''
    temp = [[] for i in range(m+1)]
    for key, value in dict.items():
        for i, v in enumerate(value[n:]):
            temp[i].append(v)
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


def _bbranking(scores, players):
    """
    Format the scores from the scores dict in the proper order of
    all players in all games (players
    Returns a list of the scores
    [48, 47, None, 60]
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
    csv_writer.writerows(l1.values())
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
    try:
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
        return (True)
    except:
        return (False)


if __name__ == "__main__":
    main()
