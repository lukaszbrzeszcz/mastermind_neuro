import ai.neuralnetwork as nn
import numpy as np
from ai.bot import Bot
from mastermind import Mastermind
import copy

import random


def shake(bot):
    layers_weights = bot.brain.get_weights()
    #print(layers_weights)
    for layer in range(len(layers_weights)):
        for x in range(len(layers_weights[layer])):
            for y in range(len(layers_weights[layer][x])):
                layers_weights[layer][x][y] *= (10 * np.random.randn() + 1)
    bot.brain.set_weights(layers_weights)
    #print(bot.brain.get_weights())

if __name__ == "__main__":
    bot = Bot(4, 8, 8, name="Marek")
    bot2 = Bot(4, 8, 8, name="Hanka")
    solution = [random.randint(1, 8) for i in range(4)]
    mm = Mastermind(4, 8, solution)
    mm2 = Mastermind(4, 8, solution)
    score = mm.play_bot(bot)
    mm2.play_bot(bot2)
    # print(bot.brain.get_weights())
    # print(bot2.brain.get_weights())
    shake(bot)


