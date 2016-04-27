"""Defines functions for the counter-factual regret algorithm
These functions are for The Resistance"""

#constants for which side we're on
RES = 0
SPY = 1

NUM_ROUNDS = 5

SPY_ALLOCATIONS = [chr(ord('a')+i) for i in range(10)]
MISSIONS = [chr(ord('A')+i) for i in range(10)]
MISSION_RESULTS = ["1","0"]
PASS, FAIL = MISSION_RESULTS

#---ESSENTIAL FUNCTIONS---

def terminal(history):
    """Returns true if the game can be evaluated at this node"""
    # a state is terminal iff it has three passes/fails or it is after the 4th mission proposed
    if history.count(PASS) == 3 or history.count(FAIL) == 3:
        return True
    # if history is spy alloc + 4 rounds of result/mission, we're also done
    if len(history) == 1 + 2*4:
        return True
    return False

def get_utility(history):
    """Returns the utility of history
    Can only be called on a terminal node"""

def get_information_set(history):
    """Returns the information set for the next player of history"""
    pass

def get_information_sets():
    """Returns all possible information sets
    Used for settuping up variables"""
    all_info_sets = []
    #spy ones start with a spy allocation
    spy_round_zero = SPY_ALLOCATIONS
    all_info_sets.extend(spy_round_zero)
    spy_last_round = spy_round_zero
    for i in range(NUM_ROUNDS-2):
        spy_round_i = []
        for m in MISSIONS:
            for r in MISSION_RESULTS:
                for i in spy_last_round:
                    spy_round_i.append(i+r+m)
        spy_last_round = spy_round_i
        all_info_sets.extend(spy_round_i)
    #resistance ones don't have a spy allocation
    res_round_zero = MISSION_RESULTS
    all_info_sets.extend(res_round_zero)
    res_last_round = res_round_zero
    for i in range(NUM_ROUNDS-1):
        res_round_i = []
        for m in MISSIONS:
            for r in MISSION_RESULTS:
                for i in res_last_round:
                    res_round_i.append(i+m+r)
        res_last_round = res_round_i
        all_info_sets.extend(res_round_i)
    """
    #terminal nodes add one extra mission
    terminal_missions = []
    for m in MISSIONS:
        for i in res_last_round:
            terminal_missions.append(i+m)
    all_info_sets.extend(terminal_missions)
    """
    return all_info_sets

def get_next_player(history):
    """Returns the next player to play (either RES or SPY)"""
    pass

def chance_node(history):
    """Returns true if history ends in a chance node"""
    return history==[]

#TODO: this should probably be memoized, unless it takes too much space, in which case
# we should probably optimize it somehow
def get_available_actions(I):
    """Returns the set of all actions which can be taken out of I"""
    if terminal(I):
        return []
    # if it's a spy strategy
    if I[0] in SPY_ALLOCATIONS:
        # check to see if a spy is part of the mission
        pass
        # check to see if passing would cause us to lose (if so, we should always fail)
        pass
    else:
        # we just treat all missions as viable
        return MISSIONS
