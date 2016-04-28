from __future__ import division
from res_cfr_fns import terminal, chance_node, get_information_set, get_available_actions,\
                        get_next_player, get_utility
from res_constants import *

def evaluate_spy_best_strategy(history, strategy):
    if terminal(history):
        return get_utility(history, SPY)
    elif chance_node(history):
        overall_val = 0
        num_available_actions = len(get_available_actions(history))
        for a in get_available_actions(history):
            overall_val += evaluate_spy_best_strategy(history+a, strategy)
        return overall_val / num_available_actions
    I = get_information_set(history)
    available_actions = get_available_actions(I)
    next_player = get_next_player(history)
    utility = 0
    if next_player == RES:
        for a in available_actions:
            utility += evaluate_spy_best_strategy(history+a, strategy)*strategy[I][a]
    else:
        for a in available_actions:
            a_utility = evaluate_spy_best_strategy(history+a, strategy)
            utility = max(utility, a_utility)
    return utility

def evaluate_mixed_strategy(history, strategy):
    if terminal(history):
        return get_utility(history, SPY)
    elif chance_node(history):
        overall_val = 0
        num_available_actions = len(get_available_actions(history))
        for a in get_available_actions(history):
            overall_val += evaluate_mixed_strategy(history+a, strategy)
        return overall_val / num_available_actions
    I = get_information_set(history)
    available_actions = get_available_actions(I)
    next_player = get_next_player(history)
    utility = 0
    for a in available_actions:
        utility += evaluate_mixed_strategy(history+a, strategy)*strategy[I][a]
    return utility

def get_p(utility):
    return (utility+1)*0.5

filename = "stored_CFR_solution_200.txt"
if __name__ == "__main__":
    import json
    json_text = open(filename).read()
    strategy = json.loads(json_text)
    best_response = evaluate_spy_best_strategy("", strategy)
    print "Spies best response wins with probability {0}".format(get_p(best_response))
    av_response = evaluate_mixed_strategy("", strategy)
    print "If both parties play the mixed response, spies win with probability {0}".format(get_p(av_response))
