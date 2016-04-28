"""Implementation of the counter-factual regret algorithm, as described in
http://modelai.gettysburg.edu/2013/cfr/cfr.pdf"""
from __future__ import division

from res_cfr_fns import terminal, get_utility, get_information_set, get_information_sets,\
                           get_next_player, chance_node, get_available_actions, evaluate_chance_node

#map of information set : regret
regret = {}
#list of strategy profiles for each time step
last_profile = {}
current_profile = {}
strategy = {}
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

    #this only works with uniform chance nodes - otherwise, this section will need to be reconsidered
    elif chance_node(history):
        #this may be the wrong thing to do
        overall_val = 0
        num_available_actions = len(get_available_actions(history))
        for a in get_available_actions(history):
            # Barak: We divide both pi_1 and pi_2 by 10 because, since neither is able
            # to 'affect'/'choose' the outcome of a chance node, the 'counterfactual'
            # probs are the same as the real probs?

            # for our problem there are always 10 choices where this happens.
            overall_val += CFR(history+a, player, time, pi_1 / num_available_actions, pi_2 / num_available_actions)
        return overall_val / num_available_actions

    I = get_information_set(history)
    available_actions = get_available_actions(I)
    v_strat = 0
    v_strat_a = {a:0 for a in available_actions}
    next_player = get_next_player(history)

    for a in available_actions:
        if next_player == P1:
            v_strat_a[a] = CFR(history+a, player, time, last_profile[I][a]*pi_1, pi_2)
        else:
            v_strat_a[a] = CFR(history+a, player, time, pi_1, last_profile[I][a]*pi_2)
        v_strat = v_strat+last_profile[I][a]*v_strat_a[a]

    if next_player == player:
        for a in available_actions:
            if player == P1:
                pi_excl_i, pi_i = pi_2, pi_1
            else:
                pi_excl_i, pi_i = pi_1, pi_2
            regret[I][a] = regret[I][a] + pi_excl_i*(v_strat_a[a]-v_strat)
            strategy[I][a] = strategy[I][a] + pi_i*last_profile[I][a]
        current_profile[I] = update_profile(I)

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
    for I in I_s:
        available_actions = get_available_actions(I)
        regret[I] = {a:0 for a in available_actions}
        strategy[I] = {a:0 for a in available_actions}
        last_profile[I] = {a:1.0/len(available_actions) for a in available_actions}

import time
start_time = time.time()
T = 2000
filename = "stored_CFR_solution_{0}.txt"
"""Runs CFR for T iterations"""
setup_CFR(T)
for t in range(T+1):
    for i in [P1, P2]:
        val_root_node = CFR("",i,t,1,1)
    print "Iteration {0} with value at root {1}".format(t, val_root_node)
    last_profile = current_profile 
    current_profile = {}

average = lambda x: sum(x) / len(x)
final_profile = {}
for I in strategy:
    sum_I = sum(strategy[I][a] for a in strategy[I])
    final_profile[I] = {a:strategy[I][a]/sum_I for a in strategy[I]}

f = open(filename.format(T),'w')
import json
s = json.dumps(final_profile)
f.write(s)
print "Finished running - ran for {0} seconds".format(time.time() - start_time)
