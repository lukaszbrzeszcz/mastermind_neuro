#! /usr/bin/python3
import numpy as np
import random

class Mastermind:
    def __init__(self, cols, rows, solution):
        self.cols = cols
        self.rows = rows
        self.board = np.zeros((self.rows, self.cols), dtype=int) 
        self.hints = np.zeros((self.rows, self.cols), dtype=int) 
        self.round = self.rows - 1
        self.solution = solution 
        self.win = False

    def board(self):
        return self.board

    def show(self):
        print('')
        print('       BOARD       |   HINTS   ')
        print('-------------------+-----------')
        for i in range(self.rows):
            for j in range(self.cols):
                print('{:4}'.format(self.board[i][j]), end = '')
            print('   | ', end = '')
            for j in range(self.cols):
                print('{:2}'.format(self.hints[i][j]), end = '')
            print('')

        #print(
        #    '\n'.join(
        #        [''.join(
        #            ['{:4}'.format(item) for item in np.append(row,row2)]
        #            ) for row, row2 in zip(self.board, self.hints)
        #        ]
        #        )
        #    )

    def play(self):
        self.show()
        while(self.round >= 0):
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

        hint = hint + [0]*(self.cols - len(hint))
        return hint

    def play_bot(self, bot):
        self.show()
        while(self.round >= 0):
            current_solution = bot.think(self.board, self.hints)
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

if __name__ == "__main__":
    mm = Mastermind(4,8,[random.randint(1,8) for i in range(4)])
    #mm = Mastermind(4,8,[1,2,3,4])
    mm.play()
