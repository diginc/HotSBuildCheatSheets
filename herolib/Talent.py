class Talent:
    def __init__(self, position, talent_name, description, games_played, popularity, win_percentage, image_name):
        self._position = position
        self._talent_name = talent_name
        self._description = description
        self._games_played = games_played
        self._popularity = popularity
        self._win_percentage = win_percentage
        self._image_name = image_name

    @property
    def position(self):
        return self._position

    @property
    def talent_name(self):
        return self._talent_name

    @property
    def description(self):
        return self._description

    @property
    def games_played(self):
        return self._games_played

    @property
    def popularity(self):
        return self._popularity

    @property
    def win_percentage(self):
        return self._win_percentage

    @property
    def image_name(self):
        return self._image_name
