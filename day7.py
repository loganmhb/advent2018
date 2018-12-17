#!/usr/bin/env python3

import sys
from collections import defaultdict
import re

line_format = re.compile(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin.*')
remaining_steps = set([])
execution_order = []
dependencies = defaultdict(set)

for line in sys.stdin.readlines():
    prereq, step = line_format.match(line).groups()
    remaining_steps.add(prereq)
    remaining_steps.add(step)
    dependencies[step].add(prereq)

# part 1
# while len(remaining_steps) > 0:
#     available_steps = [step for step in remaining_steps if len(dependencies[step]) == 0]
#     next_step = sorted(available_steps)[0]
#     execution_order.append(next_step)
#     for step in dependencies.keys():
#         dependencies[step].discard(next_step)
#     remaining_steps.remove(next_step)

# part 2

def time_required(step):
    return ord(step) - 4 # + 60 seconds - 64 for the character encoding

workers = [{'ready':0, 'step': None} for _ in range(5)]
t = -1
execution_order = []

while len(remaining_steps) > 0 or len(list(filter(lambda w: w['step'] is not None, workers))) > 0:
    t += 1
    print('t', t)
    print(workers)
    # record completed steps
    for worker in workers:
        if worker['ready'] == t and worker['step'] is not None:
            completed = worker['step']
            print('completed', completed)
            worker['step'] = None
            execution_order.append(completed)
            for step in dependencies.keys():
                dependencies[step].discard(completed)

    # start available steps
    available_steps = [step for step in remaining_steps if len(dependencies[step]) == 0]
    available_steps.sort()
    for worker in workers:
        if worker['step'] is None and len(available_steps) > 0:
            next_step = available_steps.pop(0)
            print('starting step', next_step)
            worker['step'] = next_step
            worker['ready'] = t + time_required(next_step)
            remaining_steps.remove(next_step) # it's not completed, but it's no longer in the queue

print(''.join(execution_order))
print(t)
