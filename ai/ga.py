from ai.bot import Bot
from mastermind import Mastermind

import numpy as np
import random


def play_game(bots_list):
    solution = [random.randint(1, 8) for i in range(4)]
    for bot in bots_list:
        mm = Mastermind(4, 8, solution)
        hints_table = mm.play_bot(bot, show_board=False)
        bot.score = fitness_function(hints_table)


def shake(bot):
    layers_weights = bot.brain.get_weights()
    for layer in range(len(layers_weights)):
        for x in range(len(layers_weights[layer])):
            for y in range(len(layers_weights[layer][x])):
                layers_weights[layer][x][y] *= (10 * np.random.randn() + 1)
    bot.brain.set_weights(layers_weights)


def make_population(n):
    bots_list = []
    for x in range(n):
        bot = Bot(4, 8, 8)

        # mm = Mastermind(4, 8, [random.randint(1, 8) for i in range(4)])
        # hints_table = mm.play_bot(bot, show_board=False)
        # bot.score = fitness_function(hints_table)
        shake(bot)
        bots_list.append(bot)

    return bots_list


def crossover_layers_weights(bots_list):
    layers_weights = bots_list[0].brain.get_weights()
    layers_weights_2 = bots_list[0].brain.get_weights()
    for i, layer in enumerate(bots_list[0].brain.get_weights()):
        layer_shape = layer[0].shape
        layer_size = layer[0].size
        parent_1 = layer[0].reshape(layer_size, )
        parent_2 = bots_list[1].brain.get_weights()[i][0].reshape(layer_size, )
        random_index = random.randint(0, layer_size-1)
        layer_weights = list(parent_1)[:random_index] + list(parent_2[random_index:])
        layer_weights_2 = list(parent_2[random_index:]) + list(parent_1)[:random_index]
        layers_weights[i][0] = np.array(layer_weights).reshape(layer_shape[0], layer_shape[1])
        layers_weights_2[i][0] = np.array(layer_weights_2).reshape(layer_shape[0], layer_shape[1])
    return layers_weights, layers_weights_2

def mutate_weights(l1, l2):
    l1, l2 = l1.copy(), l2.copy()
    l1[0][0][random.randint(0,16)] *= 1 + np.random.randn() * 10
    l2[0][0][random.randint(0,16)] *= 1 + np.random.randn() * 10
    return l1, l2

def make_next_generation(bots_lists):
    new_bots_list = []
    n = len(bots_list)
    bots_list.sort(key=lambda x: x.score)
    two_best = bots_list[-2:]
    for x in range(int(n/2)-1):
        bot = Bot(4, 8, 8)
        bot_2 = Bot(4, 8, 8)
        layer_weights, layer_weights_2 = crossover_layers_weights(two_best)
        layer_weights, layer_weights_2 = mutate_weights(layer_weights, layer_weights_2)
        bot.brain.set_weights(layer_weights)
        bot_2.brain.set_weights(layer_weights_2)
        #shake(bot)
        #shake(bot_2)
        new_bots_list.append(bot)
        new_bots_list.append(bot_2)
    new_bots_list.append(two_best[0])
    new_bots_list.append(two_best[1])
    return new_bots_list


def fitness_function(hints_table):
    rounds, code_size = hints_table.shape
    winner = False
    winning_round = None  # 0, 1, ...
    for i, row in enumerate(hints_table):
        if all(hint == 2 for hint in list(row)):
            winner = True
            winning_round = i
            break

    if winner:
        # winning round: 8 -> *(8-7+1) -> *2
        return sum(np.resize(hints_table, (1, hints_table.size))[0]) * (
            rounds - winning_round + 1
        )
    else:
        return sum(np.resize(hints_table, (1, hints_table.size))[0])


if __name__ == "__main__":
    bots_list = make_population(100)
    play_game(bots_list)
    print([bot.score for bot in bots_list])
    scores = []
    print("Max score: ", max(bot.score for bot in bots_list))
    # print(bots_list[0].brain.get_weights()[0][1])
    for i in range(100):
        bots_list = make_next_generation(bots_list)
        play_game(bots_list)
        max_score = max(bot.score for bot in bots_list)
        print([bot.score for bot in bots_list])
        print("Max score: ", max_score)
        scores.append(max_score)
    print(max(scores))


    # print(bots_list[0].brain.get_weights())
    # print("---NEW BOT----")
    # new_bot = Bot(4, 8, 8, brain=bots_list[-1].brain)
    # for x in range(5):
    #     mm = Mastermind(4, 8, [random.randint(1, 8) for i in range(4)])
    #     score = mm.play_bot(new_bot, show_board=False)
    #     print(score)
