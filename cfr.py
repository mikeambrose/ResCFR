"""Implementation of counter-factual regret"""
import random
#constants for which side we're on
RES = 0
SPY = 1

NUM_ROUNDS = 5

#map of information set : regret
regret = {}
#list of strategy profiles for each time step
profiles = []
#all spy allocations
SPY_ALLOCATIONS = [chr(ord('a')+i) for i in range(10)]
MISSIONS = [chr(ord('A')+i) for i in range(10)]
MISSION_RESULTS = ["1","0"]
PASS, FAIL = MISSION_RESULTS

def CFR(history, player, time, pi_1, pi_2):
    if terminal(history):
        return get_utility(history)
    # our only chance node is the first node
    elif chance_node(history):
        a = random.choice(SPY_ALLOCATIONS)
        return CFR(history+a, player, time, pi_1, pi_2)

    I = get_information_set(history)
    available_actions = get_available_actions(I)
    v_strat = 0
    v_strat_a = {a:0 for a in available_actions}
    next_player = get_next_player(history)

    for a in available_actions:
        if next_player == RES:
            v_strat_a[a] = CFR(history+a, player, time, profiles[t][I][a]*pi_1, pi_2)
        else:
            v_strat_a[a] = CFR(history+a, player, time, pi_1, profiles[t][I][a]*pi_2)
        v_strat = v_strat+profiles[t][I][a]*v_strat_a[a]

    if next_player == player:
        for a in available_actions:
            if player == RES:
                pi_excl_i, pi_i = pi_2, pi_1
            else:
                pi_excl_i, pi_i = pi_1, pi_2
            regret[I][a] = regret[I][a] + pi_excl_i*(v_strat_a[a]-v_strat)
            #cumulative strategy tables?
        #update profile
        profile[t+1][I] = update_profile(I)

    return v_strat

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
    pass

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

def update_profile(I):
    """Finds new strategy profile based on global regrets and information set I"""
    pass

def setup_CFR(T):
    """Initializes global variables"""
    I_s = get_information_sets()
    for t in range(T+1):
        profiles.append({})
    first_round_strategy = {}
    for I in I_s:
        available_actions = get_available_actions(I)
        regret[I] = {a:0 for a in available_actions}
        profiles[0][I] = {a:1.0/len(available_actions) for a in available_actions}
        for t in range(T+1):
            profiles[t][I] = {}
    profiles.append(first_round_strategy)

def solve_CFR(T):
    setup_CFR(T)
    for t in range(1,T+1):
        for i in [RES, SPY]:
            val_root_node = CFR([],i,t,1,1)
            print val_root_node

solve_CFR(1000)
