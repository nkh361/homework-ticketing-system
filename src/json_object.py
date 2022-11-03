import json, os
from datetime import date
from os import path
from dataclasses import dataclass

@dataclass
class ticket:
    username: str
    assignment: str
    start_date: str
    due_date: str
    priority: str