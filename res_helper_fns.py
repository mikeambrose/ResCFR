"""Constructs the table to determine whether spies can vote on a round"""
from res_constants import *
import itertools
letter_to_pos = {}
for pos,letter in zip(itertools.combinations(range(NUM_PLAYERS),2),MISSIONS):
    letter_to_pos[letter] = set(pos)

def spy_on_mission(mission, alloc, three_person_mission):
    """Returns true if spy allocation ALLOC leads to a spy on mission MISSION"""
    mission_people = letter_to_pos[mission]
    spy_people = letter_to_pos[alloc.upper()]
    if three_person_mission:
        mission_people = set(range(NUM_PLAYERS)) - mission_people
    return len(mission_people & spy_people) != 0

def get_current_round(h):
    """Returns the current round given the history
    for spies, this can be called with I, since they have perfect information"""
    return len(h)//2
