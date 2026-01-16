from Persistence.IStorable import IStorable


class HiddenSettings(IStorable):
    def __init__(self):
        self.version = 1
        self.defensiveKanjiReadings = False
        self.fastCardUpdate = True

    def toDictionary(self):
        return {"version": self.version, "defensiveKanjiReadings": self.defensiveKanjiReadings, "fastCardUpdate": self.fastCardUpdate}

    def fromDictionary(self, dictionary):
        version = dictionary["version"]  # do not set member!

        if version >= 1:
            self.defensiveKanjiReadings = dictionary["defensiveKanjiReadings"]
            # self.fastCardUpdate = dictionary["fastCardUpdate"]
