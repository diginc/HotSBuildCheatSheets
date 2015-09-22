class TalentSorter:
    @staticmethod
    def sort(talents, sort_key, by_position=False):
        sorted_talents = []
        for level, level_talents in sorted(talents.items()):
            sorted_tier = sorted(level_talents, key=lambda talent: getattr(talent, sort_key), reverse=True)[0]
            if by_position:
                sorted_talents.append(sorted_tier.position)
            else:
                sorted_talents.append(sorted_tier)
        return sorted_talents
