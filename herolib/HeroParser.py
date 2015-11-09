import requests
import re

from bs4 import BeautifulSoup

from herolib.Talent import Talent
from herolib.TopBuild import TopBuild

DEBUG = False
# DEBUG = True

TIER_TO_LEVEL = [1, 4, 7, 10, 13, 16, 20]


class HeroParser:
    def __init__(self, hero_url):
        self.html = BeautifulSoup(requests.get(hero_url, verify=True).text, 'lxml')
        self.talents = self.parse_talent_list()
        self.top_builds = self.parse_top_builds(self.talents)

    def parse_talent_list(self):
        """ Scrape any useful data out of the full talent list table """
        talents = {}
        raw_talents = self.html.find(id='ctl00_MainContent_RadGridHeroTalentStatistics_ctl00').tbody
        level = 0
        position = 0
        for row in raw_talents.find_all('tr'):
            if HeroParser.row_is_start_of_new_tier(row):
                position = 1
                match_object = re.match('Level: (\d+)', row.find('span', attrs={'class': 'rgGroupHeaderText'}).string)
                if match_object and match_object.group(1) not in talents:
                    level = int(match_object.group(1))
                    talents[level] = []
            else:
                talent_image_row = row.td.next_sibling.next_sibling
                talent_name = talent_image_row.next_sibling
                description = talent_name.next_sibling
                games_played = description.next_sibling
                _popularity = games_played.next_sibling
                _win_percentage = _popularity.next_sibling
                popularity = float(_popularity.string.strip(' %')) if '%' in _popularity.string else 0.0
                win_percentage = float(_win_percentage.string.strip(' %')) if '%' in _win_percentage.string else 0.0

                ''' Image name is for linking to the top winning builds '''
                talent_image = re.match('/(.*)\.png$', talent_image_row.img['src']).group(1)
                talents[level].append(Talent(position, talent_name.string,
                                             description.string, games_played.string,
                                             popularity, win_percentage, talent_image))
                position += 1
        return talents

    @staticmethod
    def row_is_start_of_new_tier(row):
        return row.attrs['class'][0] == 'rgGroupHeader'

    def parse_top_builds(self, talents):
        """ Scrape the top winning build table and
        return a usable set of data by combining it with the talent table """
        raw_builds = []
        for i in range(0, 10):
            search = 'ctl00_MainContent_RadGridPopularTalentBuilds_ctl00__' + str(i)
            raw_builds.append(self.html.find(id=search))

        top_builds = []

        for row in raw_builds:
            build_by_talent_positions = []
            build_by_talent_images = []
            games_played = row.td
            _win_percentage = games_played.next_sibling
            win_percentage = _win_percentage.string if '%' in _win_percentage.string else '??.? %'

            for column in row.find_all('img', ):
                ''' imgName as a key works better than alt text
                        because of colons in talent names '''
                match_object = re.match('/(.*)\.png$', column.attrs['src'])
                if match_object:
                    talent_image = match_object.group(1)
                    build_by_talent_images.append(talent_image)
                    for talent in talents[TIER_TO_LEVEL[len(build_by_talent_positions)]]:
                        if talent_image == talent.image_name:
                            build_by_talent_positions.append(talent.position)
            top_builds.append(TopBuild(games_played.string, win_percentage,
                                       build_by_talent_positions, build_by_talent_images))

        return top_builds
