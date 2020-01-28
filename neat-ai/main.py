"""
MasterMind - NEAT
"""

from __future__ import print_function
import os
import neat
import numpy as np
import random
from mastermind import Mastermind
import pickle


def fitness_function(hints_table):
    winner = False
    winning_round = None  # 0, 1, ...
    for i, row in enumerate(hints_table):
        if all(hint == 2 for hint in list(row)):
            winner = True
            winning_round = i
            break

    if winner and winning_round < 6:    # lucky win in first round
        return 4 * (winning_round + 1) * 20
    else:
        return sum(np.resize(hints_table, (1, hints_table.size))[0])


def eval_genomes(genomes, config):
    solution = [random.randint(1, 4) for i in range(4)]
    solution_2 = [random.randint(1, 4) for i in range(4)]
    solution_3 = [random.randint(1, 4) for i in range(4)]
    solution_4 = [random.randint(1, 4) for i in range(4)]
    for genome_id, genome in genomes:
        genome.fitness = 0.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        ## master mind
        mm = Mastermind(4, 8, solution)
        mm_2 = Mastermind(4, 8, solution_2)
        mm_3 = Mastermind(4, 8, solution_3)
        mm_4 = Mastermind(4, 8, solution_4)
        hints_table = mm.play_neat_bot(net, show_board=False, win_show=False)
        hints_table_2 = mm_2.play_neat_bot(net, show_board=False, win_show=False)
        hints_table_3 = mm_3.play_neat_bot(net, show_board=False, win_show=False)
        hints_table_4 = mm_4.play_neat_bot(net, show_board=False, win_show=False)
        genome.fitness += float(fitness_function(hints_table))
        genome.fitness += float(fitness_function(hints_table_2))
        genome.fitness += float(fitness_function(hints_table_3))
        genome.fitness += float(fitness_function(hints_table_4))


def run(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    p = neat.Population(config)
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-304')

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    winner = p.run(eval_genomes, 1000)

    filename = 'winner_nn'
    outfile = open(filename, 'wb')
    pickle.dump(winner, outfile)
    outfile.close()


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat.config')
    run(config_path)