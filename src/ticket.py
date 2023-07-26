from dataclasses import dataclass
import time, random

@dataclass
class Ticket:
    user_id: str
    assignment: str
    created_date: str
    due_date: str
    priority: str
    status: str
    ticket_id: str = None
    project_name: str = None

    def __post_init__(self):
        if self.ticket_id is None:
            self.ticket_id = self.create_ticket_id()
    
    def create_ticket_id(self):
        timestamp = int(time.time())
        rand = random.randint(1, 1000)
        ticket_id = '%d-%d' % (timestamp, rand)
        return ticket_id