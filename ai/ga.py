from ai.bot import Bot
from mastermind import Mastermind

import numpy as np
import random


def make_population(n):
    bots_list = []
    for x in range(n):
        bot = Bot(4, 8, 8)
        mm = Mastermind(4, 8, [random.randint(1, 8) for i in range(4)])
        hints_table = mm.play_bot(bot, show_board=False)
        bot.score = fitness_function(hints_table)
        bots_list.append(bot)

    return bots_list


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
    bots_list = make_population(300)
    print("Max score: ", max(bot.score for bot in bots_list))
    bots_list.sort(key=lambda x: x.score)
    two_best = bots_list[-2:]
    for bot in two_best:
        print(bot.score)
    # print("---NEW BOT----")
    # new_bot = Bot(4, 8, 8, brain=bots_list[-1].brain)
    # for x in range(5):
    #     mm = Mastermind(4, 8, [random.randint(1, 8) for i in range(4)])
    #     score = mm.play_bot(new_bot, show_board=False)
    #     print(score)
