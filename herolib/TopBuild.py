class TopBuild:
    def __init__(self, games_played, win_percentage, build_by_talent_positions, build_by_talent_image_names):
        self._games_played = games_played
        self._win_percentage = win_percentage
        self._build_by_talent_positions = build_by_talent_positions
        self._build_by_talent_image_names = build_by_talent_image_names

    @property
    def games_played(self):
        return self._games_played

    @property
    def win_percentage(self):
        return self._win_percentage

    @property
    def build_by_talent_positions(self):
        return self._build_by_talent_positions

    @property
    def build_by_talent_image_names(self):
        return self._build_by_talent_image_names
