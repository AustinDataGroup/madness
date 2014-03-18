#! /usr/bin/env python

from enum import Enum

class RankedTeamsEnum(Enum):
    team_id = 0
    rank = 1

class RankedTeams:
    @staticmethod
    def find_ranks(conn):
        sql = "select * from ranked_teams"
        results = conn.executeCommand(sql)
        returned_teams = {}
        for team in results:
            returned_teams[team[RankedTeamsEnum.team_id]] = team
        return returned_teams

    @staticmethod
    def insert_team(conn, id, team):
        sql = "insert into ranked_teams(id, team_id) VALUES (%d, %d);" % (id, team)
        conn.execute(sql)

    @staticmethod
    def rank_teams(team1, team2, team_count):
        return .5 + (.5 * (team2 - team1) / float(team_count))
