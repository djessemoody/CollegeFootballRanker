# This scrapes the records of FBS teams from the NCAA website.
#modified from wesbarnett/cfb record Scraper

from lxml import html
import requests
import sys


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
	schedteams = schedtree.xpath('//div[@class="team"]//a/@href')
	for y in range(0,len(schedteams)):
		schedteams[y] = schedteams[y][9:]
	finalscores = schedtree.xpath('//td[@class="final score"]/text()')
        if len(finalscores) == 0:
            print
            return

	gameStatus = schedtree.xpath('//div[starts-with(@class,"game-status")]/text()')


	for y in range(0,len(schedteams)):
		if schedteams[y].lower() not in allteams:
			allteams.append(schedteams[y].lower())

	x = 0

	for y in range(0,len(schedteams)-1,2):
		if (gameStatus[y/2] != "canceled"):
			if int(finalscores[x]) > int(finalscores[x+1]):
				f.write(schedteams[y].rstrip().lower().replace(" ","")+' AWAYWINOVER ')
				f.write(schedteams[y+1].rstrip().lower().replace(" ",""))
				if (week == 'P'):
					f.write(' P\n')
				else:
					f.write(' ' + str(week) + ' \n')
			else:
				f.write(schedteams[y+1].rstrip().lower().replace(" ","")+' HOMEWINOVER ')
				f.write(schedteams[y].rstrip().lower().replace(" ",""))
				if (week == 'P'):
					f.write(' P\n')
				else:
					f.write(' ' + str(week) + ' \n')
			x += 2


#for arg in sys.argv:
#    print arg

thisweek = 15;
year = sys.argv[1]
year = int(year)

allteams = []
f = open("winslosses.txt","w")
ftwo = open("teams.txt","w")
for week in range(1,thisweek+1):
    doScraping(f,year,str(week))
if year != 2015:
	doScraping(f,year,'16')
	doScraping(f,year,'P')
allteams = sorted(allteams)
for y in range(0,len(allteams)):
	ftwo.write(allteams[y].rstrip().replace(" ","")+'\n')
#doScraping(f,year,"P")

f.close();
