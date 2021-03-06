from pypokerengine.players import BasePokerPlayer
import random as rand
from pypokerengine.utils.card_utils import estimate_hole_card_win_rate
import pprint
import math

NUMBERS = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
SUITS = ['C','D','H','S']

#Train the weights here
WEIGHT_ROYAL_FLUSH = 100
WEIGHT_STRAIGHT_FLUSH = 80
WEIGHT_FOUR_OF_A_KIND = 70
WEIGHT_FULL_HOUSE = 60
WEIGHT_FLUSH = 50
WEIGHT_STRAIGHT = 40
WEIGHT_THREE_OF_A_KIND = 30
WEIGHT_TWO_PAIR = 20
WEIGHT_PAIR = 10
WEIGHT_HIGHCARD = 5

weight_raise_1 = 1
weight_raise_2 = 1
weight_raise_3 = 1
weight_raise_4 = 1
weight_raise_5 = 1

weight_fold_1 = 2
weight_fold_2 = 2
weight_fold_3 = 2
weight_fold_4 = 2
weight_fold_5 = 2




class PlayerV3(BasePokerPlayer):
    def __init__(self, weights):
        self.weights = weights
        self.weight_raise_1 = 1
        self.weight_raise_2 = 1
        self.weight_raise_3 = 1
        self.weight_raise_4 = 1
        self.weight_raise_5 = 1

        self.weight_fold_1 = 2
        self.weight_fold_2 = 2
        self.weight_fold_3 = 2
        self.weight_fold_4 = 2
        self.weight_fold_5 = 2

    def declare_action(self, valid_actions, hole_card, round_state):
        total_weight = 0


        #=======================FEATURE 1: HAND GOODNESS===========================
        weight_1 = 0
        cards = hole_card + round_state["community_card"]
        nums = {}
        for n in NUMBERS:
            nums[n] = 0
            for card in cards:
                if card[1] == n:
                    nums[n] += 1
        h_num = h2_num = h_card = h2_card = 0
        for card, num in nums.items():
            if num > h_num:
                h2_num = h_num
                h2_card = h_card
                h_num = num
                h_card = card
            elif num > h2_num:
                h2_num = num
                h2_card = card
        if h_num > 1:
            #We have at least a pair.
            prob = 1
            if h_num == 4:
                weight_1 += WEIGHT_FOUR_OF_A_KIND
            elif 7 - len(cards) >= 4 - h_num: # num of remaining unknown cards is >= num required to have FOUR_OF_A_KIND
                # Four of a kind
                if h_num == 2:
                    weight_1 += nCr(52 - len(cards) - 2, 7 - len(cards) - 2) * WEIGHT_FOUR_OF_A_KIND
                else: # h_num == 3
                    weight_1 += nCr(52 - len(cards) - 1, 7 - len(cards) - 1) * WEIGHT_FOUR_OF_A_KIND

            if h_num == 3:
                #assign P(four of a kind) weight
                if h2_num >= 2:
                    #assign full house
                    weight_1 = weight_1 # TODO: Replace this
                else:
                    #assign three of a kind
                    weight_1 = weight_1 # TODO: Replace this
            if h_num == 2:
                weight_1 = weight_1 # TODO: Replace this

        cols = {}
        for s in SUITS:
            cols[s] = 0
            for card in cards:
                if card[0] == s:
                    cols[s] += 1
        h_num = h2_num = h_card = h2_card = 0
        for num, card in nums.items():
            if num > h_num:
                h2_num = h_num
                h2_card = h_card
                h_num = num
                h_card = card
            elif num > h2_num:
                h2_num = num
                h2_card = card
        if h_num > 1:
            # We have at least two cards of the same suit.
            weight_1 = weight_1  # TODO: Replace this
            # h_num
        runs = {}

        # For straights
        for r in range(0,9):
            checked = []
            for card in cards:
                if NUMBERS[r] <= card[1] <= NUMBERS[(r+5)%13] and card[1] not in checked:
                    checked.append(card[1])
                    runs[r] = 1
        h_num = h_card = 0
        for num, card in nums.items():
            if num > h_num:
                h_num = num
                h_card = card
        if h_num > 1:
            #We have a chance of getting a straight.
            weight_1 = weight_1  # TODO: Replace this

        # high card
        # put this into pair, three of a kind, full house

        #=======================FEATURE 2: OUR BID AMOUNT===========================
        weight_2 = 0

        bid_amt = 0
        for stage in round_state["action_histories"].values():
            if len(stage) != 0 and stage[0]["uuid"] == self.uuid:
                bid_amt += stage[0]["amount"]
        # More bid amount, the less likely to fold.

        #=======================FEATURE 3: RAISE_OVER_RUN RATIO===========================
        action = ""
        weight_3 = 0

        round_state["action_histories"].values()[0].reverse()
        for stage in round_state["action_histories"].values()[0]:
            if stage["uuid"] != self.uuid:
                action = stage["action"]
                break

        if action == "RAISE" :
            opp_raise = 1
            opp_call = 1
            opp_fold = 1

            for stage in round_state["action_histories"].values()[0]:
                if stage["uuid"] != self.uuid :
                    if stage["action"] == "CALL" :
                        opp_call += 1
                    elif stage["action"] == "RAISE" :
                        opp_raise += 1
                    else :
                        opp_fold += 1
                weight_3 += 100 * (opp_fold + opp_call + opp_raise)/ (opp_fold + opp_call)




        #=======================FEATURE 4: RANDOMNESS===========================
        # To make our actions less predictable
        weight_4 = rand.random()

        #=======================FEATURE 5: If can check dont fold===========================
        # Is this part of algo or feature?

        total_raise_weight = weight_1 * weight_raise_1
        total_fold_weight = 0
        total_call_weight = 0

        if total_fold_weight > 0 and total_raise_weight > 0 :
           call_action_info = valid_actions[1]
        elif total_fold_weight > 0 and total_raise_weight < 0 :
            call_action_info = valid_actions[0]
        elif total_fold_weight < 0 and total_raise_weight > 0 :
            call_action_info = valid_actions[2]
        else :
            call_action_info = valid_actions[1]





        # past #
        #if you can check, then you should never fold
        r = rand.random()
        if r <= 0.5:
            call_action_info = valid_actions[1]
        elif r<= 0.9 and len(valid_actions ) == 3:
            call_action_info = valid_actions[2]
        else:
            call_action_info = valid_actions[0]
        action = call_action_info["action"]
        return action  # action returned here is sent to the poker engine

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


def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

def setup_ai():
    return RandomPlayer()