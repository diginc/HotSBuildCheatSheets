import requests
import re
from bs4 import BeautifulSoup
from collections import namedtuple

DEBUG=False

HEROES = [
    "Abathur",     "Anub'arak",   "Arthas",           "Azmodan",
    "Brightwing",  "Chen",        "Diablo",           "E.T.C.",
    "Falstad",     "Gazlowe",     "Illidan",          "Jaina",
    "Johanna",     "Kael'thas",   "Kerrigan",         "Leoric",
    "Li Li",       "Malfurion",   "Muradin",          "Murky",
    "Nazeebo",     "Nova",        "Raynor",           "Rehgar",
    "Sgt. Hammer", "Sonya",       "Stitches",         "Sylvanas",
    "Tassadar",    "The Butcher", "The Lost Vikings", "Thrall",
    "Tychus",      "Tyrael",      "Tyrande",          "Uther",
    "Valla",       "Zagara",      "Zeratul"
]

if DEBUG: HEROES = [ "Zagara" ]

TIERTOLEVEL=[ 1,4,7,10,13,16,20 ]

class TalentSort(object):
    def popularity(self, hero, num=False):
        sortedBuild = []
        for level,talents in hero.talents.iteritems():
            sortedTeir=sorted(talents, key=lambda tup: tup[5], reverse=True)[0]
            if num:
                sortedBuild.append(sortedTeir.number)
            else:
                sortedBuild.append(sortedTeir)
        return sortedBuild


class HeroParser(object):
    def __init__(self, hero):
        source = 'https://www.hotslogs.com/Sitewide/HeroDetails?Hero=' + hero
        if DEBUG: source = 'http://diginc.us/HeroDetails.html?Hero=' + hero
        self.html = BeautifulSoup(requests.get(source, verify=False).text, 'lxml')
        self.talents = self.parse_talent_list()
        self.topBuilds = self.parse_top_builds(self.talents)

    def parse_talent_list(self):
        ''' Scape any useful data out of the full talent list table '''
        Talent = namedtuple('Talent', 'number, talentName, description, gamesPlayed, popularity, winPercent, imgName')
        talents = {}
        rawTalents = self.html.find(id='ctl00_MainContent_RadGridHeroTalentStatistics_ctl00').tbody
        level = 0
        for row in rawTalents.find_all('tr'):
            if self.row_is_start_of_new_tier(row):
                i = 1
                m = re.match('Level: (\d+)', row.find('span', attrs={'class': 'rgGroupHeaderText'}).string)
                if m and m.group(1) not in talents:
                    level = int(m.group(1))
                    talents[level] = []
            else:
                talentImgRow=row.td.next_sibling.next_sibling
                talentName=talentImgRow.next_sibling
                description=talentName.next_sibling
                gamesPlayed=description.next_sibling
                popularity=gamesPlayed.next_sibling
                winPercent=popularity.next_sibling
                # Image name is for linking to the top winning builds
                talentImg=re.match('/(.*)\.png$', talentImgRow.img['src']).group(1)
                talents[level].append(
                    Talent(i, talentName.string,
                           description.string, gamesPlayed.string,
                           popularity.string,
                           float(winPercent.string.strip(' %')),
                           talentImg
                    )
                )
                i = i + 1
        return talents

    def row_is_start_of_new_tier(self, row):
        return row.attrs['class'][0] == 'rgGroupHeader'

    def parse_top_builds(self, talents):
        ''' Scrape the top winning build table and 
        return a usable set of data by combining it with the talent table '''
        rawBuilds = []
        for i in range(0, 10):
            search = 'ctl00_MainContent_RadGridPopularTalentBuilds_ctl00__' + str(i)
            rawBuilds.append(self.html.find(id=search))


        TopBuild = namedtuple('TopBuild', 'gamesPlayed, winPercent, buildByNum, buildByImgName')
        builds = {}
        i = 0

        for row in rawBuilds:
            #print i, ':', row
            m = None
            buildNums = []
            buildImgs = []
            gamesPlayed = row.td
            winPercent = gamesPlayed.next_sibling

            for column in row.find_all('img',):
                buildImg = None
                ''' imgName as a key works better than alt text
                        because of colons in talent names '''
                m = re.match('/(.*)\.png$', column.attrs['src'])
                if m:
                    buildImg = m.group(1)
                    buildImgs.append(buildImg)
                    #print(TIERTOLEVEL[len(buildNums)], '\n')
                    for talent in talents[TIERTOLEVEL[len(buildNums)]]:
                        if buildImg == talent.imgName:
                            buildNums.append(talent.number)
            builds[i] = TopBuild(gamesPlayed.string, winPercent.string,
                         buildNums, buildImgs)
            i = i+1

        return builds
