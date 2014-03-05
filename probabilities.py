#!/usr/bin/python

# date: 03/03/2014

from enum import Enum
from connection import PostgresConnection

from regular_season import *
from teams import *

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

##### CLASSES FOR TABLES
class Seasons:
    @staticmethod
    def find_all_seasons(conn):
        return conn.executeCommand('select * from seasons;')

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
                team1_prob, team2_prob = RegularSeason.find_probabilities(conn, team1['team_id'], team2['team_id'])
                print "team1 %f vs team2 %f" % (team1_prob, team2_prob)
                print 'Probability of %d playing %d is %f' % (team1['team_id'], team2['team_id'], team1['probability'] * team2['probability'])
