# ResCFR
This is code which implements CFR for the game of The Resistance. The code priorities readability and simplicity over raw speed (hence the Python implementation) and is suitable for small games. If you're looking for a poker-like game, [PyCFR](https://github.com/tansey/pycfr) might suit your needs better. However, if you have a reasonably small (<10^7 information sets can probably be run) game, this will suit your needs.

In order to use it on your game, you shouldn't need to modify `cfr.py`. Instead, follow the structure set in `res_cfr_fns.py` but modify them for your own game. The structure is based off the algorithm specification [here](http://modelai.gettysburg.edu/2013/cfr/cfr.pdf).

Histories are represented as strings where each character is a state. The following functions need to be implemented:

* `terminal(history)`
  * boolean function for whether or not `history` represents a final state of the game
* `get_utility(history, i)`
  * returns the utility for player `i` at terminal state `history`
* `get_information_set(history, i)`
  * returns the information set from the perspective of player `i` of `history`
* `get_information_sets()`
  * returns all information sets (used for initialization only - the implementation in `res_cfr_fns.py` will likely work for you with some tweaking)
* `get_next_player(history)`
  * returns the next player to play after `history` has occurred
* `chance_node(history)`
  * boolean function for whether or not `history` represents a chance node
* `get_available_actions(I)`
  * returns the available actions given information set `I`

In order to run your code, run `cfr.py`. The possible flags are explained by running `cfr.py -h`. We recommend using pypy instead of default python for a significant speedup.
