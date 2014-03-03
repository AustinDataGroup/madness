March Madness
=======
### Austin Data Group

#### What is this?
This is a place to hold scripts that we have written that are publicly available for helping to solve the March Madness problem.
______________

#### What is solved here?
The code here solves several issues revolving around making guesses for March Madness listed below:

**queries/** holds several database queries most notably for updating a table with all the previous march madness tournament slots with the winning and losing teams.
This is important because it allows us to see how well teams do in the tournament.

**probabilities.py** runs through all of the tournament slots and creates a python dictionary with the probabilities of a team making that level. Currently the probabilities are purely based on distance to the slot in a 50/50 probability at each step.
______________
#### What is left to do?

* Update the probabilities to look at how the teams have done against each other in the past in regular season
* Update the probabilities with which team is the strongseed and which is the weakseed.
______________

#### How do I run the queries?
To get all the data, you will need to visit the [Kaggle March Madness page](http://www.kaggle.com/c/march-machine-learning-mania/data) and download all the data and create tables for each of the csv files created there as well as one for tournament_slots_results which will house the slots with their results.
