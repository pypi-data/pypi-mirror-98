import requests
import dateutil.parser
from .urls import addParam, user, getAvatar, getRankImage
from .records import getRecords
from .base import Base
from .badges import getBadges

class User(Base):
    def __init__(self, data):
        self.ts = None
        super().__init__(data)
        self.league = LeagueData(data['league'])
        if self.ts:
            self.createdat = dateutil.parser.parse(self.ts)
        else:
            self.createdat = 'not tracked'
        if 'badges' in self.__dict__.keys():
            self.badges = getBadges(self.badges)
    
    def getAvatar(self):
        return getAvatar(self.id)
    
    def emojiFlag(self):
        out = ''
        if not self.country:
            return None
        letters = '🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿'
        for letter in self.country:
            out +=letters[ord(letter) - 65]
        return out
    
    def getRecords(self):
        return getRecords(self.username)

class LeagueData(Base):
    def __init__(self, data):
        super().__init__(data)

    def getRankImage(self):
        return getRankImage(self.rank)

def getUser(name):
    url = user
    url = addParam(url, name)
    with requests.Session() as ses:
        resp = ses.get(url).json()
        if not resp['success']:
            raise Exception(resp['error'])
    json = resp['data']['user']
    return User(json)