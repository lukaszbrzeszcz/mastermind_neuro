import pickle
import neat
import numpy as np
import random
from mastermind import Mastermind

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

with open("winner_nn", "rb") as f:
    winner = pickle.load(f)

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         "neat.config")
winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
solution = [random.randint(1, 8) for i in range(4)]
solution = [2,1,1,5]
mm = Mastermind(4, 8, solution)
game_board = np.concatenate((mm.board/8, mm.hints/2))   # normalize input
nn_input = [x for y in game_board.tolist() for x in y]
prediction_result = winner_net.activate(nn_input)
hints_table = mm.play_neat_bot(winner_net, show_board=True)


# p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-299')
# p.run(eval_genomes, 10)


