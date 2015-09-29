from operator import attrgetter

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
        def strengthpass(self,xvalue):
            for game in self.games:
                if (game.postseason == True):
                    if (self.name == game.hometeam.name):
                        if (game.result == 0):
                            self.strength += 2.0*min(game.awayteam.strength,0)/xvalue
                        else:
                            self.strength -= 1.0*min(game.awayteam.strength,0)/xvalue

                    if (self.name == game.awayteam.name):
                        if (game.result ==1):
                            self.strength += 2.0*min(game.hometeam.strength,0)/xvalue
                        else:
                            self.strength -= 1.0*min(game.hometeam.strength,0)/xvalue
                elif (self.name == game.hometeam.name):
                    if (game.result == 0):
                        self.strength += 1.0*min(game.awayteam.strength,0)/xvalue
                    else:
                        self.strength -= 1.0*min(game.awayteam.strength,0)/xvalue

                elif (self.name == game.awayteam.name):
                    if (game.result ==1):
                        self.strength += 1.0*min(game.hometeam.strength,0)/xvalue
                    else:
                        self.strength -= .75*min(game.hometeam.strength,0)/xvalue


        def showdataonotherteams(self):
            for game in self.games:
                print ("home team: " +game.hometeam.name + " " + str(game.hometeam.strength) +" "+ game.awayteam.name + " "+ str(game.awayteam.strength)+ " "+ str(game.result))
class Game:
    def __init__(self,hometeam,awayteam,result):
            self.hometeam = hometeam
            self.awayteam = awayteam
            self.result = result
            self.postseason = False


gamestextlist = list(open("winslosses.txt","r"))
teamstextlist = list(open("teams.txt","r"))






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
    hometeam.games.append(gamerec)
    awayteam.games.append(gamerec)

for team in teamsList:
    team.startingstrength()




xval=1000
for _ in range(xval):
    for team in teamsList:
        team.strengthpass(xval)


teamsList = sorted(teamsList,key=attrgetter('strength'),reverse=True)
listsize = 25
i = 1
for team in teamsList[:listsize]:
    #print(vars(team).items())
    print('#' +  str(i) + ': ' + team.name + ': record: ' + str(team.wins) + '-' + str(team.losses) + ": Strength=" + str(team.strength))
    i+=1
    team.showdataonotherteams()
