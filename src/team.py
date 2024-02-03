from dataclasses import dataclass
import time, random

@dataclass
class Team:
    project_id: str
    user_id: str
    role_id: str
    team_id: str = None

    def __post_init__(self):
        if self.team_id is None:
            self.team_id = self.create_team_id()

    def create_team_id(self):
        timestamp = int(time.time())
        team_id = '%d-%s' % (timestamp, self.owner)
        return team_id