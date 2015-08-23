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

TEIRTOLEVEL=[ 1,4,7,10,13,16,20 ]

class TalentSort(object):
    def popularity(self, hero, num=False):
        sortedBuild = []
        for level,talents in hero.talents.iteritems():
            sortedTeir=sorted(talents, key=lambda tup: tup[5])[0]
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
        self.topBuilds = self.parse_top_builds()
        self.topBuildNums = self.talent_names_to_numbers(self.topBuilds,
                                                         self.talents)

    def talent_names_to_numbers(self, topBuilds, talents):
        topBuildNums = {}
        for rank, build in topBuilds.iteritems():
            if rank not in topBuildNums:
                topBuildNums[rank] = []

            for k,v in enumerate(build):
                for talent in talents[TEIRTOLEVEL[k]]:
                    if v in talent:
                        topBuildNums[rank].append(talent.number)

        return topBuildNums


    def parse_talent_list(self):
        Talent = namedtuple('Talent', 'number, talent, description, gamesPlayed, popularity, winPercent')
        talents = {}
        rawTalents = self.html.find(id='ctl00_MainContent_RadGridHeroTalentStatistics_ctl00').tbody
        level = 0
        for row in rawTalents.find_all('tr'):
            if row.attrs['class'][0] == 'rgGroupHeader':
                i = 1
                m = re.match('Level: (\d+)', row.find('span', attrs={'class': 'rgGroupHeaderText'}).string)
                if m and m.group(1) not in talents:
                    level = int(m.group(1))
                    talents[level] = []
            else:
                talent=row.td.next_sibling.next_sibling.next_sibling
                description=talent.next_sibling
                gamesPlayed=description.next_sibling
                popularity=gamesPlayed.next_sibling
                winPercent=popularity.next_sibling
                talents[level].append(
                    Talent(i, talent.string,
                           description.string, gamesPlayed.string,
                           popularity.string, winPercent.string) )
                i = i + 1
        return talents

    def parse_top_builds(self):
        ''' todo update the builds to include talent number ? '''
        rawBuilds = []
        for i in range(0, 9):
            search = 'ctl00_MainContent_RadGridPopularTalentBuilds_ctl00__' + str(i)
            rawBuilds.append(self.html.find(id=search))

        builds = {}
        i = 1
        for row in rawBuilds:
            m = None
            if i not in builds: builds[i] = []
            for column in row.find_all('img',):
                m = re.match('([^:]*):(.*)', column.attrs['alt'])
                if m:
                    builds[i].append(m.group(1))
            i = i+1
        return builds
