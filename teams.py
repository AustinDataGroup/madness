#! /usr/bin/env python

from enum import Enum

class TeamEnum(Enum):
    id = 0
    name = 1
    
class Teams:
   @staticmethod
   def find_all_teams(conn):
        sql = 'select * from teams;' 
        return conn.executeCommand(sql)
