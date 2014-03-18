#!/usr/bin/python

# date: 03/03/2014
# version: 0.1.2

from enum import Enum
from connection import PostgresConnection

from regular_season import *
from teams import *
from ranked_teams import *
import numpy as np

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
    @staticmethod
    def find_latest_season(conn):
        return conn.executeCommand('select * from seasons order by season DESC LIMIT 1;')

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
    def find_next_match(conn, seed, season):
        sql = 'select * from tournament_slots where (strongseed = \'%s\' or weakseed = \'%s\') and season = \'%s\';' %(seed, seed, season)
        return conn.executeFindOneCommand(sql)

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

def multi_probs(all_teams, team1, team2, slot):
    prob1 = 0
    prob2 = 0
    for x in all_teams[team1]:
        if x['getting_to'] == slot:
            prob1 = x['probability']
            break
    for x in all_teams[team2]:
        if x['getting_to'] == slot:
            prob2 = x['probability']
            break

    return prob1 * prob2

if __name__ == '__main__':
    conn = PostgresConnection()

    #seasons = Seasons.find_all_seasons(conn)
    seasons = Seasons.find_latest_season(conn)

    curr_season = seasons[0][SeasonEnum.season].strip()

    teams = Teams.find_all_teams(conn)

    team_count = len(teams)

    all_slots = {}
    all_teams = {}

    ranked_teams = RankedTeams.find_ranks(conn)

    #iterate over all the teams to find out what their possible slots are for a given season.
    for team in teams:    
        team_id = team[TeamEnum.id] #cache the team's ID
        #iterate over each season
        for season in seasons:
            season_letter = season[SeasonEnum.season] #cache the season letter

            # find all the possible slots for this team.
            possible_slots = TournamentSlots.find_possible_slots_for_team(conn, team_id, season_letter)

            # if the team didn't make the tournament this season, this will be None
            if possible_slots:
                for num, slot in enumerate(possible_slots):
                    slot = slot.strip()
                    #season_slot = "%s_%s" % (season_letter.strip(), slot)
                    #season_slot = season_slot.strip()

                    if team_id in all_teams:
                        all_teams[team_id].append({'getting_to': slot, 'probability': (1.0/(num+1)), 'winning': 1.0})
                    else:
                        all_teams[team_id] = [{'getting_to': slot, 'probability': (1.0/(num+1)), 'winning': 1.0}]

                    if slot in all_slots:
                        all_slots[slot].append(team_id)
                    else:
                        all_slots[slot] = [team_id]

    writer = open('S_predictions.csv', 'w')
    writer.write('id,pred\n');

    for team in all_teams:
        teams_arr = all_teams[team]
        for team_stats in teams_arr:
            winning_probs = []
            for slot in all_slots[team_stats['getting_to']]:
                if team == slot:
                    continue
                team1_rank = ranked_teams[team][RankedTeamsEnum.rank]
                team2_rank = ranked_teams[slot][RankedTeamsEnum.rank]
                winning_probs.append(RankedTeams.rank_teams(team1_rank, team2_rank, team_count))
                #print "Probability of %d vs %d is %f" %(team, slot, np.mean(winning_probs))
                team_stats['winning'] = np.mean(winning_probs)

            next_match = TournamentSlots.find_next_match(conn, team_stats['getting_to'], curr_season)
            if next_match:
                next_slot = next_match[SlotsEnum.slot].strip()
                for x in teams_arr:
                    if x['getting_to'] == next_slot:
                        x['probability'] = team_stats['probability'] * team_stats['winning']


    team_probs = {}

    for slot in all_slots:
        teams = all_slots[slot]
        for team1 in teams:
            for team2 in teams:
                if team1 == team2:
                    continue
                key = "%s_%d_%d" % (curr_season, team1, team2)
                no_dupes = "%s_%d_%d" % (curr_season, team2, team1)
                if no_dupes in team_probs:
                    continue

                perc = multi_probs(all_teams, team1, team2, slot)
                if key in team_probs:
                    team_probs[key].append(perc)
                else:
                    team_probs[key] = [perc]
    for key in team_probs:
        writer.write('%s,%f\n' % (key, np.max(team_probs[key])))
    writer.close()
