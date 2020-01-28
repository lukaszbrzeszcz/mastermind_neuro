import pickle
import neat
import numpy as np
import random
from mastermind import Mastermind
import itertools

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
            winning_round + 2
        ) * 5
    else:
        return sum(np.resize(hints_table, (1, hints_table.size))[0]) - 20


def eval_genomes(genomes, config):
    solution = [random.randint(1, 4) for i in range(4)]
    solution_2 = [random.randint(1, 4) for i in range(4)]
    for genome_id, genome in genomes:
        genome.fitness = 4.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        ## master mind
        mm = Mastermind(4, 8, solution)
        mm_2 = Mastermind(4, 8, solution_2)
        hints_table = mm.play_neat_bot(net, show_board=False)
        hints_table_2 = mm_2.play_neat_bot(net, show_board=False)
        genome.fitness += float(fitness_function(hints_table))
        genome.fitness += float(fitness_function(hints_table_2))


with open("winner_nn_7", "rb") as f:
    winner = pickle.load(f)

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     "neat.config")
winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
# p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-2')
# winner_net = p.run(eval_genomes, 2)
solution = [random.randint(1, 8) for i in range(4)]
solutions = [[1, 3, 4, 2],
             [1, 4, 1, 4],
             [2, 1, 1, 3],
             [4, 1, 3, 2]]

solutions = list(itertools.product([1, 2, 3, 4], repeat=4))
solutions = [list(sol) for sol in solutions]
how_many_win = 0

def game_won(hints_table):
    winner = False
    winning_round = None  # 0, 1, ...
    for i, row in enumerate(hints_table):
        if all(hint == 2 for hint in list(row)):
            winner = True
            winning_round = i
            break
    return winner


for s in solutions:
    mm = Mastermind(4, 8, s)
    hints_table = mm.play_neat_bot(winner_net, win_show=True, show_board=False)
    if game_won(hints_table):
        how_many_win += 1

print("NN won {0} times per {1} possible.".format(how_many_win, 256))

# p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-299')
# p.run(eval_genomes, 10)


