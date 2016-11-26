__author__ = 'Dmitry Yutkin'

import pandas as pd
import numpy as np
from collections import defaultdict

events = pd.read_csv('./blitz/course-217-events.csv')
events = events.sort_values(by=['time', 'user_id'])

structure = pd.read_csv('./blitz/course-217-structure.csv')
structure = structure.sort_values(by=['module_position', 'lesson_position', 'step_position'])

# returns - users who have return on the step
# views - users, who viewed the step at once
steps_info = {row.step_id: {'index': i, 'returns': set(), 'views': set()}
         for i, row in enumerate(structure.itertuples())}

# maps user -> sequence of visited steps
user2steps = defaultdict(list) 

for event in events.itertuples():
  user_id, step_id = event.user_id, event.step_id

  user2steps[user_id].append(step_id)

  if user_id not in steps_info[step_id]['views']:
    steps_info[step_id]['views'].add(user_id)

for user, step_seq in user2steps.items():
  
  visited_steps = set()
  
  # here we will insert i-th, only if (i-1)-th was before that
  auxilary_set = set()
  for step in step_seq:
    
    i = steps_info[step]['index']
    
    # if i and i+1 were before that, than it is return
    if i in visited_steps and i+1 in auxilary_set:
      steps_info[step]['returns'].add(user)
    else:
      visited_steps.add(i)
    
    # if i-1 was before that, than insert ith in auxilary set
    if (i - 1) in visited_steps:
      auxilary_set.add(i)

# sort by "increasing ability"
top_steps = sorted(steps_info.items(),
  key=lambda x: -(len(x[1]['returns']) / len(x[1]['views'])))

print(','.join([str(i[0]) for i in top_steps[:10]]))