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

    def update_flatfiles(self):
        ''' Human readable/consumable data '''
        with open('wiki/Home.md', 'w') as wiki:
            wiki.write(doclib.INDEX[0] + '\n\n')
            wiki.write('Hero | Shorthand Talents\n--- | ---\n')
            for name in HEROES:
                wiki.write(name +' | '+ self.format_talents_shorthand(name)+'\n')
            wiki.write('\n\n')
            wiki.write('\n\n'.join(doclib.INDEX[1:len(doclib.INDEX)]))

    def format_talents_shorthand(self, name):
        buildStr = ''
        for teir,talentNum in enumerate(self.popularBuildByNum[name]):
            if teir == 3:
                buildStr = buildStr +'-'+ str(talentNum) +'-'
            else:
                buildStr = buildStr + str(talentNum)
        return buildStr

    def format_talents_verbose(self, name):
        buildStr = ''
        for teir,talent in enumerate(self.popularBuild[name]):
            talentNum = str(talent.number)
            buildStr = buildStr + talentNum +', '+ talent.talent +'\n'
        return buildStr

    def write_verbose_builds(self, writeTo, heroNames):
        for name in heroNames:
            print name +': '+ self.format_talents_shorthand(self.popularBuildByNum[name])
            print self.format_talents_verbose(self.popularBuild[name])


if __name__ == "__main__":
    latestData = HotSLogsLog()
    latestData.update_flatfiles()

    #print latestData.heroes['Zagara'].topBuilds
    #print latestData.heroes['Zagara'].topBuildNums latestData.write_verbose_builds(None, HEROES)
