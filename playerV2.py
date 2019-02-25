from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
import random as rand
NB_SIMULATION = 100
import pprint

class PlayerV2(BasePokerPlayer):
    def __init__(self, call_t, fold_t):
        self.call_t = call_t
        self.fold_t = fold_t

    def declare_action(self, valid_actions, hole_card, round_state):
        # valid_actions format => [raise_action_pp = pprint.PrettyPrinter(indent=2)
        #pp = pprint.PrettyPrinter(indent=2)
        #print("------------ROUND_STATE(RANDOM)--------")
        #pp.pprint(round_state)
        #print("------------HOLE_CARD----------")
        #print(hole_card)
        #print("------------VALID_ACTIONS----------")
        #pp.pprint(valid_actions)
        #print("-------------------------------")
        community_card = round_state['community_card']
        w = estimate_hole_card_win_rate(NB_SIMULATION, 2, gen_cards(hole_card), gen_cards(community_card))
        #print(w)

        if w >= self.call_t and len(valid_actions) == 3:
            call_action_info = valid_actions[2] #TO RAISE
        elif w >= self.fold_t:
            call_action_info = valid_actions[1] #TO CALL
        else:
            call_action_info = valid_actions[0] #TO FOLD

        return call_action_info['action']  # action returned here is sent to the poker engine

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

def setup_ai():
    return PlayerV2(20, 20)