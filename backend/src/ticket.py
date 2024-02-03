from dataclasses import dataclass

@dataclass
class Ticket:
    user_id: str
    assignment: str
    created_date: str
    due_date: str
    priority: str
    status: str

        
