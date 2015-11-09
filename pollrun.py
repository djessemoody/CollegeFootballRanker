from operator import attrgetter
import sys
class Team:
        """Team Data"""
        def __init__(self,name,teamid):
            self.name = name
            self.teamid = teamid
            self.strength=0
            self.wins=0
            self.losses=0
            self.totalgames=0
            self.games=[]
        #def startingstrength(self):
        #    for game in games:

        def startingstrength(self):
            self.strength = self.totalgames + self.wins - self.losses
        def strengthpass(self,xvalue,weeksinyear):
            for game in self.games:
                gameweight = 0.5*game.week/weeksinyear + .5
                #gameweight = 1.0*game.week/weeksinyear
                #gameweight = 1.0
                if (game.postseason == True):

                    if (self.name == game.hometeam.name):
                        if (game.result == 0):
                            self.strength += 1.0*max(game.awayteam.strength,self.strength/weeksinyear/2)/xvalue
                        else:
                            self.strength -= 0*max(game.awayteam.strength,self.strength/weeksinyear/2)/xvalue

                    if (self.name == game.awayteam.name):
                        if (game.result ==1):
                            self.strength += 1.0*max(game.hometeam.strength,self.strength/weeksinyear/2)/xvalue
                        else:
                            self.strength -= 0.0*max(game.hometeam.strength,self.strength/weeksinyear/2)/xvalue
                elif (self.name == game.hometeam.name):

                    if (game.result == 0):
                        self.strength += gameweight*0.75*max(game.awayteam.strength,self.strength/weeksinyear/2)/xvalue
                    else:
                        self.strength -= gameweight*1.25*max(game.hometeam.strength - game.awayteam.strength,self.strength/weeksinyear/2)/xvalue

                elif (self.name == game.awayteam.name):
                    if (game.result ==1):
                        self.strength += gameweight*1.25*max(game.hometeam.strength,self.strength/weeksinyear/2)/xvalue
                    else:
                        self.strength -= gameweight*.75*max(game.awayteam.strength - game.hometeam.strength,self.strength/weeksinyear/2)/xvalue


        def showdataonotherteams(self):
            for game in self.games:
                sys.stdout.write("home team: " +game.hometeam.name + " " + str(game.hometeam.strength) +" "+ game.awayteam.name + " "+ str(game.awayteam.strength))
                if (game.result == 0):
                    sys.stdout.write("homewin\n")
                else:
                    sys.stdout.write("awaywin\n")
class Game:
    def __init__(self,hometeam,awayteam,result):
            self.hometeam = hometeam
            self.awayteam = awayteam
            self.result = result
            self.postseason = False
            self.week = 0


gamestextlist = list(open(sys.argv[1]+"/winslosses.txt","r"))
teamstextlist = list(open(sys.argv[1]+"/teams.txt","r"))






teamsList=[]

i = 1
for team in teamstextlist:
    teamsList.append(Team(team.rstrip().lower(),i))
    i += 1

for game in gamestextlist:
    game = game.rstrip().split(" ")
    if (game[1] == "HOMEWINOVER" ):
        result = 0
        for team in teamsList:
            if (team.name == game[0]):
                hometeam = team
                team.wins += 1
                team.totalgames += 1
            if (team.name == game[2]):
                awayteam = team
                team.losses += 1
                team.totalgames += 1

    elif (game[1] == "AWAYWINOVER"):
        result = 1
        for team in teamsList:
            if (team.name == game[0]):
                awayteam = team
                team.wins += 1
                team.totalgames += 1


            if (team.name == game[2]):
                hometeam = team
                team.losses += 1
                team.totalgames += 1

    else:
        raise ValueError('Invalid home away result')

    gamerec = Game(hometeam,awayteam,result)
    if (game[3] == "P"):
        gamerec.postseason = True
    else:
        gamerec.week = int(game[3])

    hometeam.games.append(gamerec)
    awayteam.games.append(gamerec)

for team in teamsList:
    team.startingstrength()



xval=5000
for _ in range(xval):
    for team in teamsList:
        team.strengthpass(xval,10)


teamsList = sorted(teamsList,key=attrgetter('strength'),reverse=True)
listsize = 25
rankingstextlist = open(sys.argv[1]+"/rankings.txt","w+")
i = 1
for team in teamsList[:listsize]:
    #print(vars(team).items())
    print('#' +  str(i) + ': ' + team.name + ': record: ' + str(team.wins) + '-' + str(team.losses) + ": Strength=" + str(team.strength))
    i+=1
    #team.showdataonotherteams()
i=1
for team in teamsList[:100]:
    rankingstextlist.write('#' +  str(i) + ': ' + team.name + ': record: ' + str(team.wins) + '-' + str(team.losses) + ": Strength=" + str(team.strength) + '\n')
    i+=1
