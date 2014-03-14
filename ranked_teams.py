#! /usr/bin/env python

from enum import Enum

class RankedTeams:
    @staticmethod
    def insert_team(conn, id, team):
        sql = "insert into ranked_teams(id, team_id) VALUES (%d, %d);" % (id, team)
        conn.execute(sql)
