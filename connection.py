#! /usr/bin/env python
import psycopg2

#this is a basic connection class for connecting to the database.
class PostgresConnection:
    def __init__(self, host='localhost', database='madness', user='dbrear'):
        self.con = psycopg2.connect(host='localhost', database='madness', user='dbrear')
        self.cur = self.con.cursor()

    def execute(self, command):
        self.cur.execute(command)

    def executeCommand(self, command):
        self.cur.execute(command)
        res = self.cur.fetchall()
        return res

    def executeFindOneCommand(self, command):
        self.cur.execute(command)
        res = self.cur.fetchone()
        return res

    def closeConnection(self):
        if self.con:
            self.con.close();
