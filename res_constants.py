#constants for which side we're on
RES = 0
SPY = 1

NUM_ROUNDS = 5
NUM_PLAYERS = 5
NUM_PASSES = 3
NUM_FAILS = 3
THREE_PERSON_ROUNDS = [False, True, False, True, True]

SPY_ALLOCATIONS = [chr(ord('a')+i) for i in range(10)]
MISSIONS = [chr(ord('A')+i) for i in range(10)]
MISSION_RESULTS = ["1","0"]
PASS, FAIL = MISSION_RESULTS
