#! /usr/bin/python3

import numpy as np
import random
import math
from itertools import product


class Mastermind:
    def __init__(self, cols, rows, solution, max_number = 6):
        self.cols = cols
        self.rows = rows
        self.board = np.zeros((self.rows, self.cols), dtype=int)
        self.hints = np.zeros((self.rows, self.cols), dtype=int)
        self.round = self.rows - 1
        self.solution = solution
        self.max_number = max_number
        self.win = False

    def board(self):
        return self.board

    def show(self):
        print('')
        print('       BOARD       |   HINTS   ')
        print('-------------------+-----------')
        for i in range(self.rows):
            for j in range(self.cols):
                print('{:4}'.format(self.board[i][j]), end='')
            print('   | ', end='')
            for j in range(self.cols):
                print('{:2}'.format(self.hints[i][j]), end='')
            print('')

        # print(
        #    '\n'.join(
        #        [''.join(
        #            ['{:4}'.format(item) for item in np.append(row,row2)]
        #            ) for row, row2 in zip(self.board, self.hints)
        #        ]
        #        )
        #    )

    def play(self):
        self.show()
        while (self.round >= 0):
            current_solution = self.get_solution()
            self.board[self.round] = current_solution
            hint = self.get_hint()
            self.hints[self.round] = hint
            self.show()
            if current_solution == self.solution:
                self.win = True
                break
            else:
                print("WRONG!")
            self.round -= 1
        if self.win:
            print("YOU WON!")
        else:
            print("GAME OVER!!!")
            print("Correct solution: {}".format(self.solution))

    def get_solution(self):
        correct_input = False
        sol = None
        while not correct_input:
            inp = input("Your guess ({} digits): ".format(self.cols))
            try:
                sol = list(map(int, inp.split(',')))
                if len(sol) == self.cols:
                    correct_input = True
            except:
                print("Provide correct numbers in format: num, num, num,...")
        return sol

    def get_hint(self):
        hint = []
        row = self.board[self.round].copy()
        sol = self.solution.copy()
        for i in range(self.cols):
            if row[i] != sol[i]:
                continue
            hint.append(2)
            sol[i] = -1
            row[i] = -1
        for i in range(self.cols):
            if sol[i] == -1:
                continue
            for j in range(self.cols):
                if sol[i] != row[j]:
                    continue
                hint.append(1)
                row[j] = -1
                break

        hint = hint + [0] * (self.cols - len(hint))
        return hint

    def play_bot(self, bot, show_board=True, win_show=True):
        # self.show()
        # print("Start playing bot: ", bot.name)
        random_input = True
        while (self.round >= 0):
            current_solution = bot.think(self.board, self.hints, random_input)
            random_input = False
            self.board[self.round] = current_solution
            hint = self.get_hint()
            self.hints[self.round] = hint
            # self.show()
            if current_solution == self.solution:
                self.win = True
                break
            # else:
            # print("WRONG!")
            self.round -= 1
        if show_board:
            self.show()
            if self.win:
                print("YOU WON!")
            else:
                print("GAME OVER!!!")
                print("Correct solution: {}".format(self.solution))
        if self.win and win_show:
            self.show()
        score = sum(np.resize(self.hints, (1, self.hints.size))[0])
        # return self.cols*self.rows*8 if self.win else score
        return self.hints

    def play_neat_bot(self, neat_net, show_board=True, win_show=True):
        random_input = True
        while (self.round >= 0):
            # current_solution = bot.think(self.board, self.hints, random_input)
            game_board = np.concatenate((self.board / 8, self.hints / 2))  # normalize input
            nn_input = [x for y in game_board.tolist() for x in y]
            prediction_result = neat_net.activate(nn_input)
            # position_1 = prediction_result[0:8].index(max(prediction_result[0:8])) + 1
            # position_2 = prediction_result[9:17].index(max(prediction_result[9:17])) + 1
            # position_3 = prediction_result[18:26].index(max(prediction_result[18:26])) + 1
            # position_4 = prediction_result[27:35].index(max(prediction_result[27:35])) + 1
            position_1 = math.ceil(prediction_result[0] * 8)
            position_2 = math.ceil(prediction_result[1] * 8)
            position_3 = math.ceil(prediction_result[2] * 8)
            position_4 = math.ceil(prediction_result[3] * 8)
            current_solution = [position_1, position_2, position_3, position_4]
            self.board[self.round] = current_solution
            hint = self.get_hint()
            self.hints[self.round] = hint
            # self.show()
            if current_solution == self.solution:
                self.win = True
                break
            # else:
            # print("WRONG!")
            self.round -= 1
        if show_board:
            self.show()
            if self.win:
                print("YOU WON!")
            else:
                print("GAME OVER!!!")
                print("Correct solution: {}".format(self.solution))
        if self.win and win_show:
            self.show()
        score = sum(np.resize(self.hints, (1, self.hints.size))[0])
        # return self.cols*self.rows*8 if self.win else score
        return self.hints

    def play_swaszek(self, show_board = True, show_win = True):
        print("                             ")
        print("      Swaszek Algorithm      ")
        print("=============================")
        print("                             ")
        print("Correct answer: %s" % (str(self.solution)))
        print("                             ")
        colors = range(1, self.max_number+1)
        colors_mult = []
        for i in range(self.cols):
            colors_mult.append(colors)

        s = list(product(*colors_mult)) # set of possible secrets

        current_solution = [1,1,2,2]
        self.board[self.round] = current_solution
        while (self.round >= 0):
            print("                             ")
            print("     Round: %d" % (self.rows - self.round))
            print("-------------------")
            print("Possibilities: %s" % (len(s)))
            print("Guess: %s" % (str(current_solution)))
            hint = self.get_hint()
            print(" Hint: %s" % (str(hint)))
            self.hints[self.round] = hint
            self.round -= 1
            if hint == [2,2,2,2]:
                self.win = True
                print("      SUCCESS")
                break
            else:
                print("     Wrong...")
                s = test_code(current_solution, s, hint)
                print("")
                current_solution = list(random.choice(s))
                self.board[self.round] = current_solution

def test_code(cur_sol, solutions, hint):
    s = list()
    for sol in solutions:
        if _get_hint(sol, cur_sol) == hint:
            s.append(sol)
    return s

def _get_hint(corr_sol, given_sol):
    hint = []
    corr_sol = list(corr_sol)
    given_sol = list(given_sol)
    size = len(corr_sol)
    for i in range(size):
        if given_sol[i] != corr_sol[i]:
            continue
        hint.append(2)
        corr_sol[i] = -1
        given_sol[i] = -1
    for i in range(size):
        if corr_sol[i] == -1:
            continue
        for j in range(size):
            if corr_sol[i] != given_sol[j]:
                continue
            hint.append(1)
            given_sol[j] = -1
            break

    hint = hint + [0] * (size- len(hint))
    return hint

if __name__ == "__main__":
    mm = Mastermind(4, 8, [random.randint(1, 9) for i in range(4)])
    # mm = Mastermind(4,8,[1,2,3,4])
    mm.play()
