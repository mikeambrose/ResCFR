"""Implementation of the counter-factual regret algorithm, as described in
http://modelai.gettysburg.edu/2013/cfr/cfr.pdf"""
from __future__ import division

from res_cfr_fns import terminal, get_utility, get_information_set, get_information_sets,\
                           get_next_player, chance_node, get_available_actions 

#map of information set : regret
regret = {}
#list of strategy profiles for each time step
profiles = []
#all spy allocations

def CFR(history, player, time, pi_1, pi_2):
    """Runs CFR on a node with history HISTORY
    only updating if PLAYER is the next player to play
    using the profile from time TIME
    where PI_1 and PI_2 are the probabilities of players playing to get to this history
    """
    if terminal(history):
        return get_utility(history)

    elif chance_node(history):
        a = evaluate_chance_node(history)
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
        profile[t+1][I] = update_profile(I)

    return v_strat

def update_profile(I):
    """Finds new strategy profile based on global regrets and information set I"""
    available_actions = get_available_actions(I)
    sum_cfr = sum(regret[I][a] for a in available_actions)
    return {a:regret[I][a]/sum_cfr for a in available_actions}

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
    for t in range(1,T+1):
        for i in range(2):
            val_root_node = CFR("",i,t,1,1)
            print val_root_node

solve_CFR(1000)
