#!/usr/bin/python

import psycopg2
import sys
from enum import Enum

# ENUMERATORS FOR FINDING COLUMNS EASIER
class SeedEnum(Enum):
    season = 0
    seed = 1
    team_id = 2

class SlotsEnum(Enum):
    season = 0
    slot = 1
    strongseed = 2
    weakseed = 3

class SeasonEnum(Enum):
    season = 0
    years = 1
    day_zero = 2
    region_w = 3
    region_x = 4
    region_y = 5
    region_z = 6

class TeamEnum(Enum):
    id = 0
    name = 1

##### CLASSES FOR TABLES
class Seasons:
    @staticmethod
    def find_all_seasons(conn):
        return conn.executeCommand('select * from seasons;')


class Teams:
   @staticmethod
   def find_all_teams(conn):
        sql = 'select * from teams;' 
        return conn.executeCommand(sql)

class TournamentSlots:
    @staticmethod
    def find_teams_by_season(conn, season):
        sql = 'select * from tournament_slots where season = \'%s\';' % season
        return conn.executeCommand(sql)

    @staticmethod
    def find_possible_slots_for_team(conn, team_id, season):
        sql = 'select * from tournament_seeds where team_id = %d and season = \'%s\';' % (team_id, season)
        team = conn.executeFindOneCommand(sql)
        positions = []
        if team:
            TournamentSlots.find_next_placement(conn, team[SeedEnum.seed], season, positions)
            return positions


    @staticmethod
    def find_next_placement(conn, seed, season, positions):
        sql = 'select * from tournament_slots where (strongseed = \'%s\' or weakseed = \'%s\') and season = \'%s\';' %(seed, seed, season)
        res = conn.executeFindOneCommand(sql)
        if res:
            positions.append(res[SlotsEnum.slot])
            slot = TournamentSlots.find_next_placement(conn, res[SlotsEnum.slot], season, positions)
            return positions + slot
        else:
            return []

#this is a basic connection class for connecting to the database.
class PostgresConnection:
    def __init__(self, host='localhost', database='madness', user='dbrear'):
        self.con = psycopg2.connect(host='localhost', database='madness', user='dbrear')
        self.cur = self.con.cursor()

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

if __name__ == '__main__':
    conn = PostgresConnection()

    seasons = Seasons.find_all_seasons(conn)

    teams = Teams.find_all_teams(conn)

    all_slots = {}

    #iterate over all the teams to find out what their possible slots are for a given season.
    for team in teams:    
        team_id = team[TeamEnum.id] #cache the team's ID
        print 'working for team %d' % team_id
        #iterate over each season
        for season in seasons:
            season_letter = season[SeasonEnum.season] #cache the season letter

            # find all the possible slots for this team.
            possible_slots = TournamentSlots.find_possible_slots_for_team(conn, team_id, season_letter)


            # if the team didn't make the tournament this season, this will be None
            if possible_slots:
                for num, slot in enumerate(possible_slots):
                    season_slot = "%s_%s" % (season_letter.strip(), slot)
                    season_slot = season_slot.strip()

                    if season_slot in all_slots:
                        all_slots[season_slot].append({'team_id': team_id, 'probability': (1.0/(num+1))})
                    else:
                        all_slots[season_slot] = [{'team_id': team_id, 'probability': (1.0/(num+1)) }]
    for slot in all_slots:
        teams_arr = all_slots[slot]
        for team1 in teams_arr:
            for team2 in teams_arr:
                if team1 == team2:
                    continue
                print 'Probability of %d playing %d is %f' % (team1['team_id'], team2['team_id'], team1['probability'] * team2['probability'])
