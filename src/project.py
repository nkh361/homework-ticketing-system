from dataclasses import dataclass
import time, random

@dataclass
class Project:
    owner: str
    name: str
    team_id: str
    project_id: str = None

    def __post_init__(self):
        if self.project_id is None:
            self.project_id = self.create_project_id()

    def create_project_id(self):
        timestamp = int(time.time())
        rand = random.randint(1, 1000)
        project_id = '%d-%d' % (timestamp, rand)
        return project_id