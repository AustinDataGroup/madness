#! /usr/bin/env python

from enum import Enum

class RegularSeasonEnum(Enum):
    season = 0
    daynum = 1
    winning_team = 2
    winning_score = 3
    losing_team = 4
    losing_score = 5
    win_location = 6
    num_ots = 7
    game_id = 8
    difference = 9

class RegularSeason:
    @staticmethod
    def find_matchups(conn, team1, team2):
        sql = """select count(id) from regular_season_results 
            where (winning_team_id = %d and losing_team_id = %d);""" % (team1, team2)
        return conn.executeFindOneCommand(sql)

    @staticmethod
    def find_probabilities(conn, team1, team2):
        team1_prob = RegularSeason.find_matchups(conn, team1, team2)
        team2_prob = RegularSeason.find_matchups(conn, team2, team1)
        return RegularSeason.get_percentages(team1_prob[0], team2_prob[0])

    @staticmethod
    def get_percentages(team1_count, team2_count):
        total = float(team1_count + team2_count)
        if total == 0:
            return (0, 0)
        return (float(team1_count) / total), (float(team2_count) / total)
    @staticmethod
    def find_loses(conn, team_id):
    	sql = "select winning_team_id, count(winning_team_id) from regular_season_results where losing_team_id = %d group by winning_team_id;" % team_id
    	return conn.executeCommand(sql)
    @staticmethod
    def find_loss_count(conn, team_id):
    	sql = "select count(losing_team_id) from regular_season_results where losing_team_id = %d;" % team_id
    	return conn.executeFindOneCommand(sql)
