"""Defines functions for the counter-factual regret algorithm
These functions are for The Resistance"""

from res_helper_fns import spy_on_mission, get_current_round
from res_constants import *
import random

def terminal(history):
    """Returns true if the game can be evaluated at this node"""
    # a state is terminal iff it has three passes/fails or it is after the 4th mission proposed
    if history.count(PASS) == NUM_PASSES or history.count(FAIL) == NUM_FAILS:
        return True
    # if history is spy alloc + 4 rounds of result/mission, we're also done
    if len(history) == 1 + 2*(NUM_ROUNDS-1):
        return True
    return False

def get_utility(history,i):
    """Returns the utility of history
    Can only be called on a terminal node"""
    # first we check if there have already been 3 passes/fails
    if history.count(PASS) == NUM_PASSES:
        return 1 if i == RES else -1
    elif history.count(FAIL) == NUM_FAILS:
        return -1 if i == RES else 1

    # if not, we must be in the final state, so we check if there's a spy on the final mission
    final_mission = history[-1]
    alloc = history[0]
    assert final_mission in MISSIONS and alloc in SPY_ALLOCATIONS
    assert history.count(PASS) == NUM_PASSES-1 and history.count(FAIL) == NUM_FAILS-1
    if spy_on_mission(final_mission, alloc, THREE_PERSON_ROUNDS[-1]):
        return -1 if i == RES else 1
    else:
        return 1 if i == RES else -1

def get_information_set(history):
    """Returns the information set for the next player of history"""
    if get_next_player(history) == SPY:
        # we don't strip anything out here - the spy has total knowledge
        return history
    else:
        # here, we remove the spy allocation
        return history[1:]

def get_information_sets():
    """Returns all possible information sets
    Used for settuping up variables"""
    all_histories = set()
    last_round_histories = set(SPY_ALLOCATIONS)
    all_histories = all_histories | last_round_histories
    this_round_histories = set()
    while last_round_histories:
        for h in last_round_histories:
            for a in get_available_actions(get_information_set(h)):
                if not terminal(h+a):
                    this_round_histories.add(h+a)
        all_histories = all_histories | this_round_histories
        last_round_histories = this_round_histories
        this_round_histories = set()
    all_info_sets = set()
    for h in all_histories:
        all_info_sets.add(get_information_set(h))
    return all_info_sets

def get_next_player(history):
    """Returns the next player to play (either RES or SPY)"""
    if history[-1] in SPY_ALLOCATIONS or history[-1] in MISSIONS:
        return SPY
    else:
        assert history[-1] in MISSION_RESULTS
        return RES

def chance_node(history):
    """Returns true if history ends in a chance node (in this case, only the first)"""
    return history == ""

def evaluate_chance_node(history):
    """Our only chance node is only the first, so we just choose a random spy allocation"""
    return random.choice(SPY_ALLOCATIONS)

def get_available_actions(I):
    """Returns the set of all actions which can be taken out of I
    In the resistance case, it just returns all missions as feasible
    In the spy case, it checks to see if the spies even have the ability to fail
    It also checks if failing would result in an instant win or if passing would result
    in an instant loss"""
    if terminal(I):
        return []
    if I == "":
        return SPY_ALLOCATIONS
    # if it's a spy strategy
    if I[0] in SPY_ALLOCATIONS:
        current_round = get_current_round(I)
        if current_round == 0:
            #first mission proposed is always A
            mission = MISSIONS[0]
        else:
            mission = I[-1]
        alloc = I[0]
        assert mission in MISSIONS
        # check to see if a spy is part of the mission (if not, the only result is pass)
        if spy_on_mission(mission, alloc, THREE_PERSON_ROUNDS[current_round]):
            # check to see if passing would cause us to lose (if so, we should always fail)
            # or if failing would cause us to win (if so, we should always fail)
            if I.count(FAIL) == NUM_FAILS-1 or I.count(PASS) == NUM_PASSES-1:
                return [FAIL]
            else:
                return [PASS, FAIL]
        else:
            return [PASS]
    else:
        # we just treat all missions as viable
        return MISSIONS
