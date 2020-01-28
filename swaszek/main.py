from mastermind import Mastermind
import random
import numpy as np
MAX_NUMBER = 6
MAX_ITER = 5000

if __name__ == '__main__':
    solution = [random.randint(1,MAX_NUMBER) for i in range(4)]
    mm = Mastermind(4, 8, solution, MAX_NUMBER)
    mm.play_swaszek()
    #results = []
    #for i in range(MAX_ITER):
    #    solution = [random.randint(1,MAX_NUMBER) for i in range(4)]
    #    mm = Mastermind(4, 8, solution, MAX_NUMBER)
    #    res = mm.play_swaszek(show_board=False, show_win=False)
    #    if res >= 0:
    #        results.append(res)

    #results.sort()
    #print("\nPlayed %d rounds" % (MAX_ITER))
    #print("Games won: %d" % (len(results)))
    #print("Games lost: %d" % (MAX_ITER - len(results)))
    #print("Min round: %d" % (min(results)))
    #print("Max round: %d" % (max(results)))
    #print("AVG round: %f" % (sum(results)/len(results)))
