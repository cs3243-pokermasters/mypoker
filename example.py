from pypokerengine.api.game import setup_config, start_poker
from randomplayer import RandomPlayer
from raise_player import RaisedPlayer
from playerV1 import PlayerV1
from playerV2 import PlayerV2
from playerV3 import PlayerV3
import csv

f = open("poker_result.csv", "w+")
'''
Get weights in this order
WEIGHT_ROYAL_FLUSH, WEIGHT_STRAIGHT_FLUSH, WEIGHT_FOUR_OF_A_KIND, WEIGHT_FULL_HOUSE,
WEIGHT_FLUSH, WEIGHT_STRAIGHT, WEIGHT_THREE_OF_A_KIND, WEIGHT_TWO_PAIR, WEIGHT_PAIR, WEIGHT_HIGHCARD
'''

weights = [[100, 80, 70, 60, 50, 40, 30, 20, 10, 5],
           [95, 75, 65, 60, 55, 35, 20, 15, 5, 3]]

results = {}
for i in range(1):
    f.write('round ' + str(i + 1))
    for j in range(i, 1):
        #TODO:config the config as our wish
        config = setup_config(max_round=10, initial_stack=10000, small_blind_amount=10)

        # Edit the players here
        config.register_player(name="F1", algorithm=PlayerV3(weights[0]))
        config.register_player(name="F2", algorithm=PlayerV3(weights[1]))

        result = start_poker(config, verbose=1)
    for player in result['players']:
        f.write(',' + player['name'] +',' + str(player['stack']) + "\n")


f.close()

"""
        f_result = ""
        for player in result['players']:
           f_result += player['name']+": "+str(player['stack'])+"  "
        results[str(i)+" "+str(j)] = f_result

        print("Completed "+str(i)+" "+str(j)+" with result "+results[str(i)+" "+str(j)])
        
print(results)
"""
