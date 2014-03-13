#! /usr/bin/env python

from connection import PostgresConnection
from regular_season import *
from teams import *
import numpy as np

MIN_ID = 501

ITERATION_COUNT = 100

# I know there's a way to do this with python but I couldn't
# find it on the plane with no wifi.
def ranked(x,y):
    if x[1] == y[1]:
        return 0
    if x[1] < y[1]:
        return 1
    return -1

if __name__ == '__main__':

    conn = PostgresConnection()
    teams = Teams.find_all_teams(conn)
    team_count = len(teams)
    loss_mat = np.zeros(shape=(team_count, team_count))

    # create an initial rank of everyone being equal.
    initial_rank = 1./team_count
    rank = initial_rank * np.ones(shape=(1, team_count))

    # iterate through all the teams and create a loss matrix
    # a loss counts for a vote for the winning team's rank.
    for team in teams:
    	team_id = team[TeamEnum.id]
    	losses = RegularSeason.find_loses(conn, team_id)

        # find the total number of times this team lost this season
        loss_count = RegularSeason.find_loss_count(conn, team_id)

        # for each of their losses add the number of losses to a team
        #  by the total number of losses (their votes for this team by their total
        #  number of votes
    	for loss in losses:
    		team_index = team_id - MIN_ID
    		loss_index = loss[0] - MIN_ID
    		loss_mat[team_index][loss_index] = float(loss[1]) / float(loss_count[0])

    for x in range(0,ITERATION_COUNT):
        rank_temp = np.dot(rank, loss_mat)
        rank = rank_temp
    ranked_teams = zip(range(MIN_ID, MIN_ID + team_count), rank[0])

    ranked_teams.sort(ranked)
    #print the top 10 ranked teams
    print ranked_teams[0:10]
