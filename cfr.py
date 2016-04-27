"""Implementation of the counter-factual regret algorithm, as described in
http://modelai.gettysburg.edu/2013/cfr/cfr.pdf"""
from __future__ import division

from res_cfr_fns import terminal, get_utility, get_information_set, get_information_sets,\
                           get_next_player, chance_node, get_available_actions, evaluate_chance_node

#map of information set : regret
regret = {}
#list of strategy profiles for each time step
profiles = []
#all spy allocations
P1 = 0
P2 = 1

def CFR(history, player, time, pi_1, pi_2):
    """Runs CFR on a node with history HISTORY
    only updating if PLAYER is the next player to play
    using the profile from time TIME
    where PI_1 and PI_2 are the probabilities of players playing to get to this history
    """
    if terminal(history):
        return get_utility(history, player)

    elif chance_node(history):
        #this may be the wrong thing to do
        overall_val = 0
        for a in get_available_actions(history):
            overall_val += CFR(history+a, player, time, 0.1*pi_1, 0.1*pi_2)
        return overall_val / len(get_available_actions(history))

    I = get_information_set(history)
    available_actions = get_available_actions(I)
    v_strat = 0
    v_strat_a = {a:0 for a in available_actions}
    next_player = get_next_player(history)

    for a in available_actions:
        if next_player == P1:
            v_strat_a[a] = CFR(history+a, player, time, profiles[time][I][a]*pi_1, pi_2)
        else:
            v_strat_a[a] = CFR(history+a, player, time, pi_1, profiles[time][I][a]*pi_2)
        v_strat = v_strat+profiles[time][I][a]*v_strat_a[a]

    if next_player == player:
        for a in available_actions:
            if player == P1:
                pi_excl_i, pi_i = pi_2, pi_1
            else:
                pi_excl_i, pi_i = pi_1, pi_2
            regret[I][a] = regret[I][a] + pi_excl_i*(v_strat_a[a]-v_strat)
            #cumulative strategy tables?
        profiles[time+1][I] = update_profile(I)

    return v_strat

def update_profile(I):
    """Finds new strategy profile based on global regrets and information set I"""
    available_actions = get_available_actions(I)
    sum_cfr = sum(max(regret[I][a],0) for a in available_actions)
    if sum_cfr <= 0:
        new_I_profile = {a:1.0/len(available_actions) for a in available_actions}
    else:
        new_I_profile = {a:max((regret[I][a]/sum_cfr),0) for a in available_actions}
    return new_I_profile

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
    profiles.append(first_round_strategy)

def solve_CFR(T):
    """Runs CFR for T iterations"""
    setup_CFR(T)
    for t in range(T+1):
        for i in [P1, P2]:
            val_root_node = CFR("",i,t,1,1)
        print "Iteration {0} with value at root {1}".format(t, val_root_node)
    average = lambda x: sum(x) / len(x)
    final_profile = {}
    for I in profiles[1]:
        final_profile[I] = {}
        for a in profiles[1][I]:
            final_profile[I][a] = average([profiles[t][I][a] for t in range(T)])
    return final_profile

T = 20
filename = "stored_CFR_solution_{0}.txt"
final_profile = solve_CFR(T)
f = open(filename.format(T),'w')
import json
s = json.dumps(final_profile)
f.write(s)
