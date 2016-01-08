import math
import doclib

from herolib.HeroParser import HeroParser
from herolib.TalentSorter import TalentSorter

DEBUG = False
# DEBUG = True

HEROES = [
         "Abathur", "Anub'arak", "Artanis", "Arthas", "Azmodan", "Brightwing",
         "Chen", "Cho", "Diablo", "E.T.C.", "Falstad", "Gall", "Gazlowe",
         "Illidan", "Jaina", "Johanna", "Kael'Thas", "Kerrigan", "Kharazim",
         "Leoric", "Li Li", "Lt. Morales", "Lunara", "Malfurion", "Muradin",
         "Murky", "Nazeebo", "Nova", "Raynor", "Rehgar", "Rexxar",
         "Sgt. Hammer", "Sonya", "Stitches", "Sylvanas", "Tassadar",
         "The Butcher", "The Lost Vikings", "Thrall", "Tychus", "Tyrael",
         "Tyrande", "Uther", "Sonya", "Valla", "Zagara", "Zeratul"
]
HERO_BASE_URL = 'https://www.hotslogs.com/Sitewide/HeroDetails?Hero='
TALENT_TABLE = '{:<6} | {:<6} | {:<9} | {}\n'

if DEBUG:
    HEROES = ["Chen"]


def update_flat_files():
    """ Human readable/consumable data """
    wiki_file = open('wiki/Home.md', 'w')
    wiki_file.write(doclib.NEWS[0])
    wiki_file.write(doclib.INDEX[0])

    for name in HEROES:
        hero_file = open('wiki/' + name + '.md', 'w')
        hero_file.write(doclib.NEWS[0])
        hero_file.write('# ' + name + '\n\n')
        wiki_file.write('\n\n# ' + name + '\n\n')
        write_talent_table_header(wiki_file, name)
        write_talent_table_header(hero_file, name)

        top_hero_popularity_talents_by_position = top_popularity_talents_by_position[name]
        top_hero_winning_talents_by_position = top_winning_talents_by_position[name]
        found_top_talent_build = False
        found_top_winning_build = False
        highest_popularity_talents_note = '* Highest popularity talents, individually'
        highest_win_percentage_talents_note = '* Highest win percentage talents, individually'

        for top_build in heroes[name].top_builds:
            heroes_fire_link = create_heroes_fire_link(name, top_build.build_by_talent_positions)
            shorthand = format_talents_shorthand(top_build.build_by_talent_positions)
            ranked_build_representation = '[{}]({})'.format(shorthand, heroes_fire_link)
            note = ''
            if top_build.build_by_talent_positions == top_hero_popularity_talents_by_position:
                note += highest_popularity_talents_note
                found_top_talent_build = True
            if top_build.build_by_talent_positions == top_hero_winning_talents_by_position:
                if note != '':
                    note += ' <br/>*'
                note += highest_win_percentage_talents_note
                found_top_winning_build = True
            line = TALENT_TABLE.format(
                top_build.games_played,
                top_build.win_percentage,
                ranked_build_representation, note
            )
            wiki_file.write(line)
            hero_file.write(line)
        if not found_top_talent_build:
            append_other_top_build(name, wiki_file, top_hero_popularity_talents_by_position,
                                   highest_popularity_talents_note)
            append_other_top_build(name, hero_file, top_hero_popularity_talents_by_position,
                                   highest_popularity_talents_note)
        if not found_top_winning_build:
            append_other_top_build(name, wiki_file, top_hero_winning_talents_by_position,
                                   highest_win_percentage_talents_note)
            append_other_top_build(name, hero_file, top_hero_winning_talents_by_position,
                                   highest_win_percentage_talents_note)

    wiki_file.write('\n\n')
    wiki_file.write('\n\n'.join(doclib.INDEX[1:len(doclib.INDEX)]))


def append_other_top_build(name, file_handler, build, note):
    heroes_fire_link = create_heroes_fire_link(name, build)
    shorthand_format = format_talents_shorthand(build)
    build_with_embedded_link = '[{}]({})'.format(shorthand_format, heroes_fire_link)
    line = TALENT_TABLE.format(
        'N/A',
        'N/A',
        build_with_embedded_link,
        note
    )
    file_handler.write(line)


def format_talents_shorthand(build):
    shorthand_build = ''
    for tier, talentNum in enumerate(build):
        if tier == 3:
            shorthand_build += '-' + str(talentNum) + '-'
        else:
            shorthand_build += str(talentNum)
    return shorthand_build


def create_heroes_fire_link(name, build):
    if name == 'E.T.C.':
        name = 'elite-tauren-chieftain'
    if name == 'Sgt. Hammer':
        name = 'sergeant-hammer'
    if name == 'Lt. Morales':
        name = 'lt-morales'
    name = name.replace("'", "") \
        .replace(" ", "-") \
        .lower()
    return 'http://www.heroesfire.com/hots/talent-calculator/' \
           + name + '#' \
           + format_talent_as_heroes_fire_hash(build)


def format_talent_as_heroes_fire_hash(build):
    heroes_fire_hash_build = '1'
    for tier, talentNum in enumerate(build):
        heroes_fire_hash_build += str(talentNum)
    residual = int(heroes_fire_hash_build)
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    radix_64 = ''
    while True:
        rixit = residual % len(alphabet)
        radix_64 = alphabet[int(math.floor(rixit))] + radix_64
        residual = math.floor(residual / len(alphabet))
        if residual == 0:
            break
    return radix_64


def format_talents_verbose(build):
    verbose_build = ''
    for tier, talent in enumerate(build):
        talent_position = str(talent.position)
        verbose_build = verbose_build + talent_position + ', ' + talent.talent + '\n'
    return verbose_build


def write_talent_table_header(file_handler, hero_name):
    hots_url = HERO_BASE_URL + hero_name
    counter_url = 'http://hotscounters.com/#/hero/' + hero_name
    file_handler.write('Links: [{}]({}) | [{}]({})\n\n'.format(
        'HOTS Logs Source', hots_url,
        'HotS Counters', counter_url
    ))
    file_handler.write(TALENT_TABLE.format('Games', 'Win %', 'Build', 'Note'))
    file_handler.write(TALENT_TABLE.format('-----', '-----', '-----', '----'))


if __name__ == "__main__":
    heroes = {}
    top_popularity_talents = {}
    top_popularity_talents_by_position = {}
    top_winning_talents_by_position = {}
    for hero in HEROES:
        hero_url = HERO_BASE_URL + hero
        current_hero = HeroParser(hero_url)
        heroes[hero] = current_hero
        top_popularity_talents[hero] = TalentSorter.sort(current_hero.talents, sort_key='popularity')
        top_popularity_talents_by_position[hero] = TalentSorter.sort(current_hero.talents,
                                                                     sort_key='popularity',
                                                                     by_position=True)
        top_winning_talents_by_position[hero] = TalentSorter.sort(current_hero.talents,
                                                                  sort_key='win_percentage',
                                                                  by_position=True)
    update_flat_files()
