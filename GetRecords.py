# This scrapes the records of FBS teams from the NCAA website.


from lxml import html
import requests

def fixTeamNames(teamnames):

	for x in range(0,len(teamnames)):
		if teamnames[x] == "Ole Miss":
			teamnames[x] = "Mississippi"
		if teamnames[x] == "C MICH":
			teamnames[x] = "Central Michigan"
		if teamnames[x] == "Mississippi St.":
			teamnames[x] = "Mississippi State"
		if teamnames[x] == "Washington St.":
			teamnames[x] = "Washington State"
		if teamnames[x] == "Colorado St.":
			teamnams[x] = "Colorado State"
		if teamnames[x] == "Northern Ill.":
			teamnames[x] = "Northern Illinois"
		if teamnames[x] == "Western Mich.":
			teamnames[x] = "Western Michigan"
		if teamnames[x] == "Eastern Mich.":
			teamnames[x] = "Eastern Michigan"
		if teamnames[x] == "Cent. Michigan":
			teamnames[x] = "Central Michigan"
		if teamnames [x] == "MIAMI":
			teamnames[x] = "Miami (Fla.)"
		if teamnames [x] == "COLO":
			teamnames[x] = "Colorado"
		if teamnames [x] == "CO ST":
			teamnames[x] = "Colorado State"
		if teamnames [x] == "OKLA":
			teamnames[x] = "Oklahoma"
		if teamnames [x] == "TENN":
			teamnames[x] = "Tennessee"
		if teamnames [x] == "S ALA":
			teamnames[x] = "South Alabama"
		if teamnames[x] == "New Mexico St.":
			teamnames[x] = "New Mexico State"
		if teamnames[x] == "Appalachian St.":
			teamnames[x] = "Appalachian State"
		if teamnames[x] == "Middle Tenn.":
			teamnames[x] = "Middle Tennessee"
		if teamnames[x] == "La.-Monroe":
			teamnames[x] = "Louisiana-Monroe"
		if teamnames[x] == "La.-Lafayette":
			teamnames[x] = "Louisiana-Lafayette"
		if teamnames[x] == "Ark.-Pine Bluff":
			teamnames[x] = "Arkansas-Pine Bluff"
		if teamnames[x] == "Jacksonville St.":
			teamnames[x] = "Jacksonville State"
		if teamnames[x] == "Western Ky.":
			teamnames[x] = "Western Kentucky"
		if teamnames[x] == "Steph. F. Austin":
			teamnames[x] = "Stephen F. Austin State"
		if teamnames[x] == "South Dakota St.":
			teamnames[x] = "South Dakota State"
		if teamnames[x] == "North Dakota St.":
			teamnames[x] = "North Dakota State"
		if teamnames[x] == "Youngstown St.":
			teamnames[x] = "Youngstown State"
		if teamnames[x] == "Central Ark.":
			teamnames[x] = "Central Arkansas"
		if teamnames[x] == "Northern Ariz.":
			teamnames[x] = "Northern Arizona"
		if teamnames[x] == "Western Caro.":
			teamnames[x] = "Western Carolina"
		if teamnames[x] == "N.C. Central":
			teamnames[x] = "North Carolina Central"
		if teamnames[x] == "NC State":
			teamnames[x] = "North Carolina State"
		if teamnames[x] == "Ga. Southern":
			teamnames[x] = "Georgia Southern"
		if teamnames[x] == "FIU":
			teamnames[x] = "Florida International"

	return teamnames

def doScraping(f,year,week):

	strweek = week
	if week != "P":
		if int(week) < 10:
			strweek = "0" + week

	SCHEDURLBASE = "http://www.ncaa.com/scoreboard/football/fbs/"
	SCHEDURL = SCHEDURLBASE + str(year) + "/" + strweek
	print " Getting results for week " + str(week) + " from " + SCHEDURL + "."

	schedpage = requests.get(SCHEDURL)
	schedtree = html.fromstring(schedpage.text)
	schedteams = schedtree.xpath('//div[@class="team"]//a/text()')
	finalscores = schedtree.xpath('//td[@class="final score"]/text()')
        if len(finalscores) == 0:
            print
            return
        else:
            print "Number of Scores for week " + `week` + ": " + `len(finalscores)`

	gameStatus = schedtree.xpath('//div[starts-with(@class,"game-status")]/text()')

	schedteams = fixTeamNames(schedteams)

	for y in range(0,len(schedteams)):
		if schedteams[y].lower() not in allteams:
			allteams.append(schedteams[y].lower())

	x = 0

	for y in range(0,len(schedteams)-1,2):
		if (gameStatus[y/2] != "canceled"):
			if int(finalscores[x]) > int(finalscores[x+1]):
				f.write(schedteams[y].rstrip().lower()+'\nAWAYWIN\n')
				f.write(schedteams[y+1].rstrip().lower()+'\n\n')
			else:
				f.write(schedteams[y+1].rstrip().lower()+'\nHOMEWIN\n')
				f.write(schedteams[y].rstrip().lower()+'\n\n')
			x += 2



thisweek = 15;
year = 2015;
allteams = []
f = open("winslosses.txt","w")
ftwo = open("teams.txt","w")
for week in range(1,thisweek+1):
    doScraping(f,year,str(week))
allteams = sorted(allteams)
for y in range(0,len(allteams)):
	ftwo.write(allteams[y].rstrip()+'\n')
#doScraping(f,year,"P")

f.close();
