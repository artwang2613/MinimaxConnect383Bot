import sys
import argparse
from agents import RandomAgent, HumanAgent, MinimaxAgent, MinimaxHeuristicAgent, MinimaxHeuristicPruneAgent
from connect383 import GameState, play_game
import test_boards

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('p1', choices=['r','h','c'])
    parser.add_argument('p2', choices=['r','h','c'])
    parser.add_argument('nrows', type=int)
    parser.add_argument('ncols', type=int)
    parser.add_argument('--prune', action='store_true')
    parser.add_argument('--depth', type=int)
    args = parser.parse_args()
    # print("args:", args)  

    players = []
    for p in [args.p1, args.p2]:
        if p == 'r':
            player = RandomAgent()
        elif p == 'h':
            player = HumanAgent()
        elif p == 'c':
            if not args.depth:
                player = MinimaxAgent()
            else:
                if not args.prune:
                    player = MinimaxHeuristicAgent(args.depth)
                else:
                    player = MinimaxHeuristicPruneAgent(args.depth)
        players.append(player)            

    
    start_state = GameState(args.nrows, args.ncols)

    results = []
    w1 = 0
    w2 = 0
    tie = 0
    for i in range(0, 100):
        results = play_game(players[0], players[1], start_state)
        if results[0] > results[1]:
            w1 += 1
        elif results[0] < results[1]:
            w2 += 1
        else:
            tie += 1
    print("P1 w%: ")
    print(w1/(w1+w2+tie))
    print("P2 w%: ")
    print(w2/(w1+w2+tie))
