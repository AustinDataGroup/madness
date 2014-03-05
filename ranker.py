#! /usr/bin/env python

from connection import PostgresConnection
from regular_season import *
from teams import *
import numpy as np

MIN_ID = 501

if __name__ == '__main__':

    conn = PostgresConnection()
    teams = Teams.find_all_teams(conn)
    team_count = len(teams)
    loss_mat = np.zeros(shape=(team_count, team_count))
    for team in teams:
    	team_id = team[TeamEnum.id]
    	losses = RegularSeason.find_loses(conn, team_id)
    	for loss in losses:
    		team_index = team_id - MIN_ID
    		loss_index = loss[0] - MIN_ID
    		loss_mat[team_index][loss_index] = float(loss[1])
    print loss_mat[329][:]