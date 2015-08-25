from herolib import HEROES, HeroParser, TalentSort
import doclib

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

    def write_shorthand_header(self, fh):
        fh.write('{:<4} | {:<9} | {}\n'.format('Rank', 'Build', 'Note'))
        fh.write('{:<4} | {:<9} | {}\n'.format('----', '-----', '----'))

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

            #heroFile.write(self.format_talents_verbose())
            for i in range(1, 11):
                rankedBuild = self.heroes[name].topBuildNums[i]
                rankedBuildStr = self.format_talents_shorthand(rankedBuild)
                note = ''
                if rankedBuild == topTalentBuildNums:
                    note = '* Highest ranked popularity talents'
                    foundTopTalentBuild = True
                line = '  {:<2d} | {:<9} | {}\n'.format(i, rankedBuildStr, note)
                wikiFile.write(line)
                heroFile.write(line)
            if not foundTopTalentBuild:
                note = '* Highest ranked popularity talents'
                topTalentBuildStr = self.format_talents_shorthand(topTalentBuildNums)
                line = '  {:<2} | {:<9} | {}\n'.format('NR', topTalentBuildStr, note)
                wikiFile.write(line)
                heroFile.write(line)

        wikiFile.write('\n\n')
        wikiFile.write('\n\n'.join(doclib.INDEX[1:len(doclib.INDEX)]))

    def format_talents_shorthand(self, build):
        buildStr = ''
        for teir,talentNum in enumerate(build):
            if teir == 3:
                buildStr = buildStr +'-'+ str(talentNum) +'-'
            else:
                buildStr = buildStr + str(talentNum)
        return buildStr

    def format_talents_verbose(self, build):
        buildStr = ''
        for teir,talent in enumerate(build):
            talentNum = str(talent.number)
            buildStr = buildStr + talentNum +', '+ talent.talent +'\n'
        return buildStr

    def write_verbose_builds(self, fh, heroNames, build):
        for name in heroNames:
            fh.write(name +': '+ self.format_talents_shorthand(build))
            fh.write(self.format_talents_verbose(build))


if __name__ == "__main__":
    latestData = HotSLogsLog()
    latestData.update_flatfiles()

    #print latestData.heroes['Zagara'].topBuilds
    #print latestData.heroes['Zagara'].topBuildNums 
    #latestData.write_verbose_builds(None, HEROES)
