from herolib import HEROES, HeroParser, TalentSorter
import math
import doclib


TALENTTABLE = '{:<6} | {:<6} | {:<9} | {}\n'

class HotSLogsLog(object):
    def __init__(self):
        self.heroes = {}
        self.topPopularityTalents = {}
        self.topPopularityTalentsByNum = {}
        self.topWinningTalentsByNum = {}
        for hero in HEROES:
            curHero = HeroParser(hero=hero)
            self.heroes[hero] = curHero
            self.topPopularityTalents[hero] = TalentSorter().sortTalentsBy(curHero.talents, sort='popularity')
            self.topPopularityTalentsByNum[hero] = TalentSorter().sortTalentsBy(curHero.talents, sort='popularity', num=True)
            self.topWinningTalentsByNum[hero] = TalentSorter().sortTalentsBy(curHero.talents, sort='winPercent', num=True)

    def update_flatfiles(self):
        ''' Human readable/consumable data '''
        wikiFile = open('wiki/Home.md', 'w')
        wikiFile.write(doclib.NEWS[0])
        wikiFile.write(doclib.INDEX[0])

        for name in HEROES:
            heroFile = open('wiki/'+ name +'.md', 'w')
            heroFile.write(doclib.NEWS[0])
            heroFile.write('# '+ name +'\n\n')
            wikiFile.write('\n\n# '+ name +'\n\n')
            self.write_talent_table_header(wikiFile, name)
            self.write_talent_table_header(heroFile, name)

            topTalentTalentNums = self.topPopularityTalentsByNum[name]
            topWinningTalentNums = self.topWinningTalentsByNum[name]
            foundTopTalentBuild = False
            foundTopWinningBuild = False
            popularStr = '* Highest win % talents, individually'
            winningStr = '* Highest popularity talents, individually'

            for i in range(len(self.heroes[name].topBuilds)):
                rankedBuild = self.heroes[name].topBuilds[i]
                heroesFireLink = self.create_hf_link(name, rankedBuild.buildByNum)
                shortHand = self.format_talents_shorthand(rankedBuild.buildByNum)
                rankedBuildStr = '[{}]({})'.format(shortHand,heroesFireLink)
                note = ''
                if rankedBuild.buildByNum == topTalentTalentNums:
                    note += popularStr
                    foundTopTalentBuild = True
                if rankedBuild.buildByNum == topWinningTalentNums:
                    if note != '': note += ' <br/>*'
                    note += winningStr
                    foundTopWinningBuild = True
                line = TALENTTABLE.format(
                    rankedBuild.gamesPlayed,
                    rankedBuild.winPercent,
                    rankedBuildStr, note
                )
                wikiFile.write(line)
                heroFile.write(line)
            if not foundTopTalentBuild:
                self.append_other_top_build(name, wikiFile,topTalentTalentNums,popularStr)
                self.append_other_top_build(name, heroFile,topTalentTalentNums,popularStr)
            if not foundTopWinningBuild:
                self.append_other_top_build(name, wikiFile,topWinningTalentNums,winningStr)
                self.append_other_top_build(name, heroFile,topWinningTalentNums,winningStr)

        wikiFile.write('\n\n')
        wikiFile.write('\n\n'.join(doclib.INDEX[1:len(doclib.INDEX)]))

    def append_other_top_build(self, name, fh, build, note):
        heroesFireLink = self.create_hf_link(name, build)
        shortHand = self.format_talents_shorthand(build)
        buildStr = '[{}]({})'.format(shortHand,heroesFireLink)
        line = TALENTTABLE.format(
            'N/A',
            'N/A',
            buildStr, note
        )
        fh.write(line)

    def format_talents_shorthand(self, build):
        buildStr = ''
        for tier,talentNum in enumerate(build):
            if tier == 3:
                buildStr = buildStr +'-'+ str(talentNum) +'-'
            else:
                buildStr = buildStr + str(talentNum)
        return buildStr

    def create_hf_link(self, name, build):
        if name == 'E.T.C.':
                name = 'elite-tauren-chieftain'
        if name == 'Sgt. Hammer':
                name = 'sergeant-hammer'
        name = name.replace("'", "") \
                   .replace(" ", "-") \
                   .lower()
        return 'http://www.heroesfire.com/hots/talent-calculator/' \
               + name + '#' \
               + self.format_talent_as_heroesfire_hash(build)

    def format_talent_as_heroesfire_hash(self, build):
        buildStr = '1'
        for tier,talentNum in enumerate(build):
            buildStr = buildStr + str(talentNum)
        buildInt = int(buildStr)
        residual = buildInt
        alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
        radix64Str = ''
        while True:
            rixit = residual % len(alphabet)
            radix64Str = alphabet[int(math.floor(rixit))] + radix64Str
            residual = math.floor( residual / len(alphabet))
            if residual == 0: break
        return radix64Str

    def format_talents_verbose(self, build):
        buildStr = ''
        for tier,talent in enumerate(build):
            talentNum = str(talent.number)
            buildStr = buildStr + talentNum +', '+ talent.talent +'\n'
        return buildStr

    def write_talent_table_header(self, fh, heroName):
        hotsUrl = 'https://www.hotslogs.com/Sitewide/HeroDetails?Hero=' + heroName
        counterUrl = 'http://hotscounters.com/#/hero/' + heroName
        fh.write('Links: [{}]({}) | [{}]({})\n\n'.format(
                'HOTS Logs Source', hotsUrl,
                'HotS Counters', counterUrl 
            )
        )
        fh.write(TALENTTABLE.format('Games', 'Win %', 'Build', 'Note'))
        fh.write(TALENTTABLE.format('-----', '-----', '-----', '----'))


if __name__ == "__main__":
    latestData = HotSLogsLog()
    latestData.update_flatfiles()
