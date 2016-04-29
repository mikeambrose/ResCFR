"""Implementation of the counter-factual regret algorithm, as described in
http://modelai.gettysburg.edu/2013/cfr/cfr.pdf"""
from __future__ import division

from res_cfr_fns import terminal, get_utility, get_information_set, get_information_sets,\
                           get_next_player, chance_node, get_available_actions

import time
import json
from decimal import *
import argparse


#map of information set : regret
regret = {}
#list of strategy profiles for each time step
last_profile = {}
current_profile = {}
strategy = {}
#all spy allocations
P1 = 0
P2 = 1
#whether or not to use Decimal
DECIMAL_ZERO = Decimal(0)
DECIMAL_ONE = Decimal(1)
FLOAT_ZERO = 0
FLOAT_ONE = 1
use_decimal = False
zero = FLOAT_ZERO
one = FLOAT_ONE

def CFR(history, player, pi_1, pi_2):
    """Runs CFR on a node with history HISTORY
    only updating if PLAYER is the next player to play
    where PI_1 and PI_2 are the probabilities of players playing to get to this history
    """
    if terminal(history):
        return get_utility(history, player)

    #this only works with uniform chance nodes - otherwise, this section will need to be reconsidered
    elif chance_node(history):
        overall_val = zero
        num_available_actions = len(get_available_actions(history))
        for a in get_available_actions(history):
            overall_val += CFR(history+a, player, pi_1, pi_2)
        return overall_val / num_available_actions

    I = get_information_set(history)
    available_actions = get_available_actions(I)
    v_strat = zero
    v_strat_a = {a:zero for a in available_actions}
    next_player = get_next_player(history)

    for a in available_actions:
        if next_player == P1:
            v_strat_a[a] = CFR(history+a, player, last_profile[I][a]*pi_1, pi_2)
        else:
            v_strat_a[a] = CFR(history+a, player, pi_1, last_profile[I][a]*pi_2)
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
    sum_pcfr = sum(max(regret[I][a],zero) for a in available_actions)
    if sum_pcfr <= 0:
        new_I_profile = {a:one/len(available_actions) for a in available_actions}
    else:
        new_I_profile = {a:max((regret[I][a]/sum_pcfr), zero) for a in available_actions}
    return new_I_profile

def setup_CFR(T):
    """Initializes global variables"""
    I_s = get_information_sets()
    for I in I_s:
        available_actions = get_available_actions(I)
        regret[I] = {a:zero for a in available_actions}
        strategy[I] = {a:zero for a in available_actions}
        last_profile[I] = {a:one/len(available_actions) for a in available_actions}



def write_strategies(T, filename, output_figures = 10):
    average = lambda x: sum(x) / len(x)
    final_profile = {}
    for I in strategy:
        sum_I = sum(strategy[I][a] for a in strategy[I])
        if use_decimal:
            final_profile[I] = {a:str((strategy[I][a]/sum_I)
                                .quantize(Decimal('.'+'0'*output_figures+'1')))
                                for a in strategy[I]}
        else:
            final_profile[I] = {a:strategy[I][a]/sum_I for a in strategy[I]}

    out_filename  = filename.format(T) if '{0}' in filename else filename
    f = open(out_filename, 'w')
    s = json.dumps(final_profile)
    f.write(s)
    return final_profile


if __name__ == "__main__":
    # argument handling
    parser = argparse.ArgumentParser(description='Solve Resistance using CFR')
    
    parser.add_argument('-T', dest='T', type=int, help='the number of rounds to run', required=True)
    parser.add_argument('-o', dest='out_file', help='output file', required=True)
    parser.add_argument('-D', dest='use_decimal', action='store_const', const=True, default=False,
                        help='whether or not to use python arbitrary-precision decimals')
    parser.add_argument('-p', dest='precision', type=int,
                        help='level of precision (only used with -D flag)', default=32)
    parser.add_argument('-op', dest='output_precision', type=int,
                        help='level of precision of output (only used with -D flag', default=16)
    parser.add_argument('-u', dest='update', action='store_const', const=True, default=False, 
                        help='write to file periodically (include {0} in your file if you choose this')
    parser.add_argument('-up', dest='update_period', type=int, default=1000,
                        help='how frequently to write to file (used with -u)')

    args = parser.parse_args()

    #globally set whether or not we're using decimal
    use_decimal = args.use_decimal
    zero = DECIMAL_ZERO if use_decimal else FLOAT_ZERO
    one = DECIMAL_ONE if use_decimal else FLOAT_ONE

    output_precision = min(args.output_precision, args.precision-2)

    if '{0}' not in args.out_file and args.update:
        print "A formatting location must be included in the output file"
    getcontext().prec = args.precision

    start_time = time.time()

    setup_CFR(args.T)
    for t in range(args.T+1):
        iter_time = time.time()
        for i in [P1, P2]:
            start_prob = DECIMAL_ONE if args.use_decimal else FLOAT_ONE
            val_root_node = CFR("",i,start_prob, start_prob)
        print "Iteration {0}/{3} with value at root {1} - took {2} seconds".format(t, val_root_node,
                                                                       time.time()-iter_time, args.T)
        last_profile = current_profile 
        current_profile = {}
        if t % args.update_period == 0 and args.update and t != 0:
            final_profile = write_strategies(t, args.out_file, output_precision)
    write_strategies(args.T, args.out_file, output_precision)
    print "Finished running - ran for {0} seconds".format(time.time() - start_time)

