import math
import itertools
from pulp import *

class Tree:
    def __init__(self):
        self.v = None
        self.p = None
        self.f = None

    def  __str__(self):
        if not self.v:
            return "None"
        s = str(self.v)
        if self.p:
            s += '\nPass: ' + str(self.p)
        if self.f:
            s += '\nFail: ' + str(self.f)
        return s

def doctest():
    success = True
    success = success and (compute_win_chance(101, 0)) == 3
    success = success and (compute_win_chance(101, 1)) == 3
    success = success and (compute_win_chance(101, 2)) == 4
    success = success and (compute_win_chance(101, 3)) == 4
    if success:
        print("Passed 10,1")
    else:
        print("Failed 10,1")
        success = True
    success = success and (compute_win_chance(27, 0)) == 4
    success = success and (compute_win_chance(27, 1)) == 4
    success = success and (compute_win_chance(27, 2)) == 1
    success = success and (compute_win_chance(27, 3)) == 1
    if success:
        print("Passed 2,7")
    else:
        print("Failed 2,7")
        success = True



"""
Bad strategies:
r1  1spy    2spy
0   pass    pass
1   pass    fail
2   fail    pass
3   fail    fail

"""

class GStrategy:
    def __init__(self, g_strategy_num):
        """
        The five players are ABCDE, and r1 always plays AB.
        If r1 passes, the 15 strategies possible are ordered as follows:
        r2  ACD (and if it fails/passes then)
        00  AB
        01  AC
        02  AE
        03  BC
        04  BE
        05  CD
        06  CE

        r2  CDE (and if it fails/passes then)
        07  AB
        08  AC
        09  CD

        r2  ABC (and if it fails/passes then)
        10  AB
        11  AC
        12  AD
        13  CD
        14  DE

        If r1 fails, good cannot play ABC. The 10 strategies possible
        are enumerated above (in the same order)
        """

        if g_strategy_num < 0 or g_strategy_num > 149:
            raise ValueError("g_strategy_num out of range")
        r1 = Tree()
        r1.v = [1,2]
        r1_pass_num = int(g_strategy_num / 10)
        r1_fail_num = g_strategy_num % 10

        r2p = Tree()
        r3p = Tree()
        r2f = Tree()
        r3f = Tree()

        def set_r2_and_r3_trees(r1_pass_num, r1_fail_num, r2p, r3p, r2f, r3f):
            if r1_pass_num < 7:
                r2p.v = [1,3,4]
                if r1_pass_num == 0:
                    r3p.v = [1,2]
                elif r1_pass_num == 1:
                    r3p.v = [1,3]
                elif r1_pass_num == 2:
                    r3p.v = [1,5]
                elif r1_pass_num == 3:
                    r3p.v = [2,3]
                elif r1_pass_num == 4:
                    r3p.v = [2,5]
                elif r1_pass_num == 5:
                    r3p.v = [3,4]
                elif r1_pass_num == 6:
                    r3p.v = [3,5]
            elif r1_pass_num < 10:
                r2p.v = [3,4,5]
                if r1_pass_num == 7:
                    r3p.v = [1,2]
                elif r1_pass_num == 8:
                    r3p.v = [1,3]
                elif r1_pass_num == 9:
                    r3p.v = [3,4]
            else:
                r2p.v = [1,2,3]
                if r1_pass_num == 10:
                    r3p.v = [1,2]
                elif r1_pass_num == 11:
                    r3p.v = [1,3]
                elif r1_pass_num == 12:
                    r3p.v = [1,4]
                elif r1_pass_num == 13:
                    r3p.v = [3,4]
                elif r1_pass_num == 14:
                    r3p.v = [4,5]

            if r1_fail_num < 7:
                r2f.v = [1,3,4]
                if r1_fail_num == 0:
                    r3f.v = [1,2]
                elif r1_fail_num == 1:
                    r3f.v = [1,3]
                elif r1_fail_num == 2:
                    r3f.v = [1,5]
                elif r1_fail_num == 3:
                    r3f.v = [2,3]
                elif r1_fail_num == 4:
                    r3f.v = [2,5]
                elif r1_fail_num == 5:
                    r3f.v = [3,4]
                elif r1_fail_num == 6:
                    r3f.v = [3,5]
            elif r1_fail_num < 10:
                r2f.v = [3,4,5]
                if r1_fail_num == 7:
                    r3f.v = [1,2]
                elif r1_fail_num == 8:
                    r3f.v = [1,3]
                elif r1_fail_num == 9:
                    r3f.v = [3,4]

            return (r2p, r3p, r2f, r3f)

        r2p, r3p, r2f, r3f = set_r2_and_r3_trees(r1_pass_num, r1_fail_num, Tree(), Tree(), Tree(), Tree())

        r2p.p = 'win'
        r2p.f = r3p
        r2f.p = r3f
        r2f.f = 'lose'

        r1.p = r2p
        r1.f = r2f

        self.tree = r1

# code for 3 round game
if True:
    """
    Bad strategies:
    r1  1spy    2spy
    0   pass    pass
    1   pass    fail
    2   fail    pass
    3   fail    fail

    """

    def compute_wins_table():
        table = []
        for g_strategy_num in range(150):
            row = []
            for b_strategy_num in range(4):
                row.append(compute_win_chance(g_strategy_num, b_strategy_num))
            table.append(row)
        return table

    def print_wins_table():
        table = compute_wins_table()
        for i in range(len(table)):
            row = table[i]
            r1_pass_num = int(i / 10)
            r1_fail_num = i % 10
            print('p: {} f: {} num_wins: {}'.format(r1_pass_num, r1_fail_num, row))

    def compute_win_chance(g_strategy_num, b_strategy_num):
        #print(GStrategy(g_strategy_num).tree)
        #print(b_strategy_num)
        num_wins = 0
        for b_loc_list in itertools.combinations([1,2,3,4,5],2):
            is_win = compute_win_given_b_loc(g_strategy_num, b_strategy_num, b_loc_list)
            #print(str(b_loc_list) + ' ' + str(is_win))
            num_wins += is_win

        return num_wins


    def compute_win_given_b_loc(g_strategy_num, b_strategy_num, b_loc_list):
        """
        Returns 1 if g_strategy_num wins against b_strategy_num given
        spy locations b_loc_list, and 0 if it loses.
        """
        b_loc_set = set(b_loc_list)
        r1_tree = GStrategy(g_strategy_num).tree
        num_passes = 0

        # round 1
        r1 = r1_tree.v
        num_bad_r1 = len(set(r1).intersection(b_loc_set))
        #print('r1 ' + str(r1) + ' blocs ' + str(b_loc_set))
        #print("num_bad_r1 = " + str(num_bad_r1))
        
        if num_bad_r1 == 0:
            r2_tree = r1_tree.p
            num_passes += 1
        elif num_bad_r1 == 1:
            if b_strategy_num < 2:
                r2_tree = r1_tree.p
                num_passes += 1
            else:
                r2_tree = r1_tree.f
        elif num_bad_r1 == 2:
            if b_strategy_num % 2 == 0:
                r2_tree = r1_tree.p
                num_passes += 1
            else:
                r2_tree= r1_tree.f
        else:
            raise ValueError("num_bad_r1 should be 0, 1, or 2")

        # round 2
        r2 = r2_tree.v
        num_bad_r2 = len(set(r2).intersection(b_loc_set))

        if num_bad_r2 == 0:
            if num_passes == 1:
                return 1
            else:
                r3_tree = r2_tree.p
                num_passes += 1
        elif num_bad_r2 > 0:
            if num_passes == 0:
                return 0
            else:
                r3_tree = r2_tree.f

        # round 3
        r3 = r3_tree.v
        num_bad_r3 = len(set(r3).intersection(b_loc_set))

        if num_bad_r3 == 0:
            return 1
        else:
            return 0

    def solve_3r_r():
        prob = LpProblem("resistance", LpMinimize)
        z = LpVariable("z")
        x0 = LpVariable("prob b strat 0", 0, 1)
        x1 = LpVariable("prob b strat 1", 0, 1)
        x2 = LpVariable("prob b strat 2", 0, 1)
        x3 = LpVariable("prob b strat 3", 0, 1)

        prob += z, "Minimum value of best response to bad guy mixed strat"
        prob += x0 + x1 + x2 + x3 == 1, "Probs sum to 1"

        table = compute_wins_table()
        for row_num in range(len(table)):
            row = table[row_num]
            prob += row[0] * x0 + row[1] * x1 + row[2] * x2 + row[3] * x3 <= z, 'good strat num {}'.format(row_num)

        prob.writeLP("resistance.lp")
        prob.solve()

        print('Status: ', LpStatus[prob.status])
        for v in prob.variables():
            print(v.name, " = ", v.varValue)

        print('Value: ' + str(value(prob.objective)))

    def solve_3r_v2():
        prob = LpProblem("resistance2", LpMaximize)
        z = LpVariable("z")
        gg_strats = list(range(150))
        gg_vars = LpVariable.dicts("gg", gg_strats, 0, 1)

        table = compute_wins_table()

        prob += z, "Maximum value of best response to good guy mixed strat"
        prob += lpSum([gg_vars[i] for i in gg_strats]) == 1, "Probs sum to 1"
        prob += lpSum([table[i][0] * gg_vars[i] for i in gg_strats]) >= z, "bad strat 0"
        prob += lpSum([table[i][1] * gg_vars[i] for i in gg_strats]) >= z, "bad strat 1"
        prob += lpSum([table[i][2] * gg_vars[i] for i in gg_strats]) >= z, "bad strat 2"
        prob += lpSum([table[i][3] * gg_vars[i] for i in gg_strats]) >= z, "bad strat 3"

        prob.writeLP("resistance2.lp")
        prob.solve()

        print('Status: ', LpStatus[prob.status])
        for v in prob.variables():
            print(v.name, " = ", v.varValue)

        print('Value: ' + str(value(prob.objective)))

# code for 5 round game
if True:
    """
    Good strategy mapping (naive)
    00  ABC
    01  AB D
    02  AB  E
    03  A CD
    04  A C E
    05  A  DE
    06   BCD
    07   BC E
    08   B DE
    09    CDE

    """

    def get_bad_loc_likelihoods_given(r1_win, r2_group, r2_win, r3_group, r3_win, bad_strategy=None):
        b_loc_set = itertools.combinations([1,2,3,4,5],2)
        if bad_strategy:
            raise NotImplementedError
        else:
            # incredibly naive, return equal prob of all possible locs
            if not r1_win: 
                for pair in b_loc_set.copy():
                    if (1 not in pair) and (2 not in pair):
                        b_loc_set.remove(pair)
            if not r2_win:
                for pair in b_loc_set.copy():
                    if (r2_group[0] not in pair) and (r2_group[1] not in pair) and (r2_group[2] not in pair):
                        b_loc_set.remove(pair)
            if not r3_win:
                for pair in b_loc_set.copy():
                    if (r3_group[0] not in pair) and (r3_group[1] not in pair):
                        b_loc_set.remove(pair)
            num_possible_locs = len(b_loc_set)
            b_loc_prob_dict = {}
            for pair in b_loc_set:
                b_loc_prob_dict[pair] = 1.0 / num_possible_locs
            return b_loc_prob_dict        

    def get_r4_r5_tree(num_wins, g_strategy_num):

        if g_strategy_num < 0 or g_strategy_num > 99:
            raise ValueError("g_strategy_num out of range")
        r4 = Tree()
        r4_num = int(g_strategy_num / 10)
        r5_num = g_strategy_num % 10

        r4.v = get_group_from_num(r4_num)

        if num_wins != 1 and num_wins != 2:
            raise ValueError("Incorrect number of wins!")
        if num_wins == 1:
            r4.f = 'lose'
            r4.p = get_group_from_num(r5_num)
        else:
            r4.p = 'win'
            r4.f = get_group_from_num(r5_num)

        return r4

    def get_group_from_num(g_strategy_num):
        if g_strategy_num == 0:
            return [1,2,3]
        if g_strategy_num == 1:
            return [1,2,4]
        if g_strategy_num == 2:
            return [1,2,5]
        if g_strategy_num == 3:
            return [1,3,4]
        if g_strategy_num == 4:
            return [1,3,5]
        if g_strategy_num == 5:
            return [1,4,5]
        if g_strategy_num == 6:
            return [2,3,4]
        if g_strategy_num == 7:
            return [2,3,5]
        if g_strategy_num == 8:
            return [2,4,5]
        if g_strategy_num == 9:
            return [3,4,5]