import sqlite3, json, os
from datetime import date
from os import path

relational_database = 'tickets.db'

class TicketObject:
    def __init__(self, assignment, due_date, priority):
        self.assignment = assignment
        self.due_date = due_date
        self.priority = priority

def main():
    to = ticket_object("test", "test date", "low")
    print(to.check_user_table())
main()
