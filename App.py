from src.json_object import json_object
from src.database import SQL_entry
from os import path
from flask import Flask, request, render_template

class Server:
    def __init__(self):
        self.test = "Hello, world!"

    def test(self):
        SQL_entry.update_entry()

def main():
    Server.test()
main()
