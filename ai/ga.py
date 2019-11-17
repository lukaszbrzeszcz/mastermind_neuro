from ai.bot import Bot
from mastermind import Mastermind

import random


def make_population(n):
    bots_list = []
    for x in range(n):
        bot = Bot(4, 8, 8)
        mm = Mastermind(4, 8, [random.randint(1, 8) for i in range(4)])
        score = mm.play_bot(bot, show_board=False)
        bot.score = score
        bots_list.append(bot)

    # for bot in bots_list:
    #     print(bot.score)

    return bots_list


if __name__ == "__main__":
    bots_list = make_population(200)
    print("Max score: ", max(bot.score for bot in bots_list))
    bots_list.sort(key=lambda x: x.score)
    two_best = bots_list[-2:]
    for bot in two_best:
        print(bot.score)
    print("---NEW BOT----")
    new_bot = Bot(4, 8, 8, brain=bots_list[-1].brain)
    for x in range(5):
        mm = Mastermind(4, 8, [random.randint(1, 8) for i in range(4)])
        score = mm.play_bot(new_bot, show_board=False)
        print(score)
