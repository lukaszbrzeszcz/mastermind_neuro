import ai.neuralnetwork as nn
import numpy as np
from ai.bot import Bot
from mastermind import Mastermind

import random


if __name__ == "__main__":
    bot = Bot(4, 8, 8)
    mm = Mastermind(4, 8, [random.randint(1, 8) for i in range(4)])
    # print('----')
    mm.play_bot(bot)
