import json
from datetime import datetime

class Match:

    def __init__(self, id, time, league, team_one, team_two, note=''):
        self.id = id
        self.time = datetime.strftime(time, "%Y-%m-%d %H:%M:%S").strip()
        self.league = league
        self.note = note
        self.team_one = team_one
        self.team_two = team_two

    def __repr__(self):
        return self.league + ": " + self.team_one + " vs. " + self.team_two + " at " + self.time

    def is_tbd(self):
        return self.team_one == "TBD" or self.team_two == "TBD"

    def to_json(self):
         return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @staticmethod
    def from_json(json):
        return Match(json['id'], datetime.strptime(json['time'], "%Y-%m-%d %H:%M:%S"), json['league'], json['team_one'], json['team_two'],json['note'])
         