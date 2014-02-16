#! /usr/bin/env python

import numpy as np
import csv
from sklearn.ensemble import RandomForestClassifier

csv_reader = csv.reader(open('data/regular_season_labeled_data.csv', 'rb'))
test_data_csv = csv.reader(open('data/testing_data.csv'))

test_data_csv.next()
print csv_reader.next()

print 'Loading the training data...',
data = []
for row in csv_reader:
    data.append(row)
print 'done!'

print 'Loading the testing data...',
test_data = []
for row in test_data_csv:
    test_data.append(row)
print 'done!'

data = np.array(data)
test_data = np.array(test_data)

Forest = RandomForestClassifier(n_estimators = 100)

print 'Fitting trees with the training data...',
Forest = Forest.fit(data[0:, 1:], data[0:, 0])
print 'done!'

print 'Predicting test data...',
Output = Forest.predict(test_data)
print 'done!'

print 'Writing predictions...',
outfile = csv.writer(open('predictions/results.csv', 'wb'))
outfile.writerow(['ndx', 'team1_won'])
for ndx, row in enumerate(Output):
    outfile.writerow([ndx+1, row])
print 'done!'
