"""
2-input XOR example -- this is most likely the simplest possible example.
"""

from __future__ import print_function
import os
import neat
import visualize
import numpy as np
import random
from mastermind import Mastermind
import pickle


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
    solution = [random.randint(1, 8) for i in range(4)]
    solution_2 = [random.randint(1, 8) for i in range(4)]
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

        # for xi, xo in zip(xor_inputs, xor_outputs):
        #     output = net.activate(xi)
        #     genome.fitness -= (output[0] - xo[0]) ** 2


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 300)

    filename = 'winner_nn'
    outfile = open(filename, 'wb')
    pickle.dump(winner, outfile)
    outfile.close()

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    # for xi, xo in zip(xor_inputs, xor_outputs):
    #     output = winner_net.activate(xi)
    #     print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

    # visualize.draw_net(config, winner, True, node_names=node_names)
    # visualize.plot_stats(stats, ylog=False, view=True)
    # visualize.plot_species(stats, view=True)

    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    p.run(eval_genomes, 10)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat.config')
    run(config_path)