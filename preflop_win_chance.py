from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
import csv

f = open("preflop_win_chance.csv", "w+")

array_H = ['HA', 'HK', 'HQ', 'HJ', 'HT', 'H9', 'H8', 'H7', 'H6', 'H5', 'H4', 'H3', 'H2']
array_D = ['DA', 'DK', 'DQ', 'DJ', 'DT', 'D9', 'D8', 'D7', 'D6', 'D5', 'D4', 'D3', 'D2']

for i in range(len(array_H)):
    for j in range(i, len(array_D)):
        print(str(array_H[i]) + str(array_D[j]))
        hole_card = gen_cards([array_H[i], array_D[j]])
        community_card = gen_cards([])

        result = estimate_hole_card_win_rate(nb_simulation = 1000000, nb_player= 2, hole_card= hole_card, community_card= community_card)

        f.write(str(result) + ",")
    f.write("\n")
    for k in range(i + 1):
        f.write(",")
f.write("\n")
for i in range(len(array_H)):
    f.write(",")
    for j in range(i + 1, len(array_H)):
        hole_card = gen_cards([array_H[i], array_H[j]])
        community_card = gen_cards([])
        print(str(array_H[i]) + str(array_H[j]))
        result = estimate_hole_card_win_rate(nb_simulation = 1000000, nb_player= 2, hole_card= hole_card, community_card= community_card)

        f.write( str(result) + ",")
    f.write("\n")
    for k in range(i + 1):
        f.write(",")
f.close()