from pypokerengine.api.game import setup_config, start_poker
from randomplayer import RandomPlayer
from raise_player import RaisedPlayer
from playerV1 import PlayerV1
from playerV2 import PlayerV2


results = {}
for i in range(10):
    for j in range(i, 10):
        #TODO:config the config as our wish
        config = setup_config(max_round=10, initial_stack=10000, small_blind_amount=10)

        config.register_player(name="F1", algorithm=PlayerV2(0.7, 0.4))
        config.register_player(name="F2", algorithm=PlayerV2(0.7, 0.35))

        result = start_poker(config, verbose=1)
        """
        f_result = ""
        for player in result['players']:
           f_result += player['name']+": "+str(player['stack'])+"  "
        results[str(i)+" "+str(j)] = f_result

        print("Completed "+str(i)+" "+str(j)+" with result "+results[str(i)+" "+str(j)])
        
print(results)
"""