__author__ = 'Dmitry Yutkin'

import pandas as pd
import numpy as np
from collections import defaultdict

events = pd.read_csv('./blitz/course-217-events.csv')
structure = pd.read_csv('./blitz/course-217-structure.csv')
events = events.sort_values(by=['time', 'user_id'])

# maps step id -> step cost
step2cost = {i['step_id']:i['step_cost']
             for i in structure[['step_id', 'step_cost']].to_dict('records')}

users = dict()
for event in events.itertuples():
  uid = event.user_id
  if uid not in users:
    users[uid] = {
      'score': step2cost[event.step_id],
      'last_action': event.time,
      'first_action': event.time,
    }

  if users[uid]['score'] < 24 and event.action == 'passed':
    users[uid]['score'] += step2cost[event.step_id]
    if users[uid]['score'] == 24:
      users[uid]['last_action'] = event.time


# only those who is passed
top = filter(lambda x: x[1]['score'] > 23, users.items())

# sort by passing duration
top = sorted(top, key=lambda y: abs(y[1]['last_action'] - y[1]['first_action']))

print(','.join([str(i[0]) for i in top[:10]]))