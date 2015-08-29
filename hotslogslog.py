from herolib import HEROES, HeroParser, TalentSort
import doclib

HEROTABLE = '{:<6} | {:<6} | {:<9} | {}\n'

class HotSLogsLog(object):
    def __init__(self):
        self.heroes = {}
        self.popularBuild = {}
        self.popularBuildByNum = {}
        for hero in HEROES:
            curHero = HeroParser(hero=hero)
            self.heroes[hero] = curHero
            self.popularBuild[hero] = TalentSort().popularity(curHero)
            self.popularBuildByNum[hero] = TalentSort().popularity(curHero, num=True)

    def update_flatfiles(self):
        ''' Human readable/consumable data '''
        wikiFile = open('wiki/Home.md', 'w')
        wikiFile.write(doclib.INDEX[0])

        for name in HEROES:
            heroFile = open('wiki/'+ name +'.md', 'w')
            heroFile.write('# '+ name +' Builds\n\n')
            wikiFile.write('\n\n# '+ name +' Builds Shorthand\n\n')
            self.write_shorthand_header(wikiFile)
            self.write_shorthand_header(heroFile)

            topTalentBuild = self.popularBuild[name]
            topTalentBuildNums = self.popularBuildByNum[name]
            foundTopTalentBuild = False

            for i in range(len(self.heroes[name].topBuilds)):
                rankedBuild = self.heroes[name].topBuilds[i]
                rankedBuildStr = self.format_talents_shorthand(rankedBuild.buildByNum)
                note = ''
                if rankedBuild.buildByNum == topTalentBuildNums:
                    note = '* Highest ranked popularity talents'
                    foundTopTalentBuild = True
                line = HEROTABLE.format(
                    rankedBuild.gamesPlayed,
                    rankedBuild.winPercent,
                    rankedBuildStr, note
                )
                wikiFile.write(line)
                heroFile.write(line)
            if not foundTopTalentBuild:
                note = '* Highest ranked popularity talents'
                topTalentBuildStr = self.format_talents_shorthand(topTalentBuildNums)
                line = HEROTABLE.format(
                    'N/A',
                    'N/A',
                    topTalentBuildStr, note
                )
                wikiFile.write(line)
                heroFile.write(line)

        wikiFile.write('\n\n')
        wikiFile.write('\n\n'.join(doclib.INDEX[1:len(doclib.INDEX)]))

    def format_talents_shorthand(self, build):
        buildStr = ''
        for tier,talentNum in enumerate(build):
            if tier == 3:
                buildStr = buildStr +'-'+ str(talentNum) +'-'
            else:
                buildStr = buildStr + str(talentNum)
        return buildStr

    def format_talents_verbose(self, build):
        buildStr = ''
        for tier,talent in enumerate(build):
            talentNum = str(talent.number)
            buildStr = buildStr + talentNum +', '+ talent.talent +'\n'
        return buildStr

    def write_shorthand_header(self, fh):
        fh.write(HEROTABLE.format('Games', 'Win %', 'Build', 'Note'))
        fh.write(HEROTABLE.format('-----', '-----', '-----', '----'))


if __name__ == "__main__":
    latestData = HotSLogsLog()
    latestData.update_flatfiles()
