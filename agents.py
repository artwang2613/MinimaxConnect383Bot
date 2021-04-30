import random
import math


BOT_NAME = "I don't know what I'm doing" 


class RandomAgent:
    """Agent that picks a random available move.  You should be able to beat it."""
    def __init__(self, sd=None):
        if sd is None:
            self.st = None
        else:
            random.seed(sd)
            self.st = random.getstate()

    def get_move(self, state):
        if self.st is not None:
            random.setstate(self.st)
        return random.choice(state.successors())


class HumanAgent:
    """Prompts user to supply a valid move."""
    def get_move(self, state, depth=None):
        move__state = dict(state.successors())
        prompt = "Kindly enter your move {}: ".format(sorted(move__state.keys()))
        move = None
        while move not in move__state:
            try:
                move = int(input(prompt))
            except ValueError:
                continue
        return move, move__state[move]


class MinimaxAgent:
    """Artificially intelligent agent that uses minimax to optimally select the best move."""

    def get_move(self, state):
        """Select the best available move, based on minimax value."""
        nextp = state.next_player()
        best_util = -math.inf if nextp == 1 else math.inf
        best_move = None
        best_state = None

        for move, state in state.successors():
            util = self.minimax(state)
            if ((nextp == 1) and (util > best_util)) or ((nextp == -1) and (util < best_util)):
                best_util, best_move, best_state = util, move, state
        return best_move, best_state

    def minimax(self, state):
        """Determine the minimax utility value of the given state.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the exact minimax utility value of the state
        """
        if state.is_full():
            return state.utility()  #hits a terminal leaf and starts back propagating the utility

        utilScores = []
        for move, state in state.successors():
            print(state)
            utilScores.append(self.minimax(state)) #recursively adding in state minimax utility scores
        if state.next_player() == 1:
            #print("max")
            return max(utilScores)
        else:
            #print("min")
            return min(utilScores)

        return 0


class MinimaxHeuristicAgent(MinimaxAgent):
    """Artificially intelligent agent that uses depth-limited minimax to select the best move."""

    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def minimax(self, state):
        """Determine the heuristically estimated minimax utility value of the given state.

        The depth data member (set in the constructor) determines the maximum depth of the game 
        tree that gets explored before estimating the state utilities using the evaluation() 
        function.  If depth is 0, no traversal is performed, and minimax returns the results of 
        a call to evaluation().  If depth is None, the entire game tree is traversed.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """
        print("doing eval")
        return self.recursionHelper(state, 0) #uses a recursion helper func, starts at a depth of 0

    def recursionHelper(self, state, curDepth):
        if curDepth is self.depth_limit-1:
            return self.evaluation(state)
        elif curDepth < self.depth_limit-1 and state.is_full(): 
            print("got to terminal")
            return state.utility() #if the current depth isnt the limit yet but we've reached a terminal leaf return utility
        
        utilScores = []
        for move, state in state.successors():
            utilScores.append(self.recursionHelper(state, curDepth + 1))
        if not utilScores:
            return 0
        else:
            if state.next_player() == 1:
                #print("max")
                return max(utilScores)
            else:
                #print("min")
                return min(utilScores)
        


    def evaluation(self, state):
        """Estimate the utility value of the game state based on features.

        N.B.: This method must run in O(1) time!
        

        Args:
            state: a connect383.GameState object representing the current board

        Returns: a heusristic estimate of the utility value of the state
        """
        #print(state)
        maxStreakC = state.num_cols
        maxStreakR = state.num_rows
        
        colCoeff = 0
        rowCoeff = 0

        if maxStreakC < maxStreakR: #higher point multiplier depending on which direction of the board is longer = longer streaks are better
            rowCoeff = 4*(maxStreakR - maxStreakC) + 4
            colCoeff = colCoeff/2
            maxVals = [0] * (maxStreakR+1)
            minVals = [0] * (maxStreakR+1)
        elif maxStreakC > maxStreakR:
            colCoeff = 4*(maxStreakC - maxStreakR) + 4
            rowCoeff = rowCoeff/2
            maxVals = [0] * (maxStreakC+1)
            minVals = [0] * (maxStreakC+1)
        else:
            colCoeff = 4
            rowCoeff = 8
            maxVals = [0] * (maxStreakR+1)
            minVals = [0] * (maxStreakR+1)

        diagCoeff = max(maxStreakC, maxStreakR)
        
        evalRet = 0
        rows = state.get_rows()
        cols = state.get_cols()
        diags = state.get_diags()

        maxCounter = 0
        minCounter = 0
        flipper = 1

        #I realized there was a more accurate way to check for potential points: not being stupid and including non open spaces
        #if they were in the way.

        #Checks for potential point streaks vertically by seeing if a current chip is boxed off from empty spaces or friendly pieces
        #Max moves increase score, min moves decrease score
        #print("Col Scoring")
        for col in range(0, len(cols)):
            maxVals[maxCounter] = maxVals[minCounter] + 1
            maxCounter = 0
            minVals[minCounter] = minVals[minCounter] + 1
            minCounter = 0
            for row in range(0, len(cols[col])):
                if flipper == 1:
                    if cols[col][row] == 1 or (cols[col][row] == 0 and maxCounter > 0):
                        maxCounter += 1
                    else:
                        flipper *= -1
                        maxVals[maxCounter] = maxVals[minCounter] + 1
                        maxCounter = 0
                if flipper == -1:
                    if cols[col][row] == -1 or (cols[col][row] == 0 and minCounter > 0):
                        minCounter += 1
                    else:
                        flipper *= -1
                        minVals[minCounter] = minVals[minCounter] + 1
                        minCounter = 0


        for i in range(1, len(maxVals)):
            evalRet += colCoeff*(maxVals[i]-minVals[i])*i
        #Checks for potential point streaks horizontally by seeing if a current chip is boxed off from empty spaces or friendly pieces
        #Max moves increase score, min moves decrease score
        #print(evalRet)
        maxCounter = 0
        minCounter = 0
        maxVals = [0]*len(maxVals)
        minVals = [0]*len(minVals)
        flipper = 1
        #print(minCounter)

        #print("Row Scoring")
        for row in range(0, len(rows)):
            maxVals[maxCounter] = maxVals[minCounter] + 1
            maxCounter = 0
            minVals[minCounter] = minVals[minCounter] + 1
            minCounter = 0
            for col in range(0, len(rows[row])):
                if flipper == 1:
                    if rows[row][col] == 1 or (rows[row][col] == 0 and maxCounter > 0):
                        maxCounter += 1
                    else:
                        flipper *= -1
                        #print("flipped")
                        #print(maxCounter)
                        maxVals[maxCounter] = maxVals[minCounter] + 1
                        #print(maxVals)
                        maxCounter = 0

                if flipper == -1:
                    if rows[row][col] == -1 or (rows[row][col] == 0 and minCounter > 0):
                        minCounter += 1
                        #print(minCounter)
                    else:
                        flipper *= -1 
                        #print("flipped")
                        #print(minCounter)
                        minVals[minCounter] = minVals[minCounter] + 1
                        #print(minVals)
                        minCounter = 0

        for i in range(1, len(maxVals)):
            evalRet += rowCoeff*(maxVals[i]-minVals[i])*i

        maxCounter = 0
        minCounter = 0
        maxVals = [0]*len(maxVals)
        minVals = [0]*len(minVals)
        flipper = 1
        #print(minCounter)

        #print("Diag Scoring")
        for diag in range(0, len(diags)):
            maxVals[maxCounter] = maxVals[minCounter] + 1
            maxCounter = 0
            minVals[minCounter] = minVals[minCounter] + 1
            minCounter = 0
            for cur in range(0, len(diags[diag])):
                if flipper == 1:
                    if  diags[diag][cur] == 1 or (diags[diag][cur] == 0 and maxCounter > 0):
                        maxCounter += 1
                    else:
                        flipper *= -1
                        #print("flipped")
                        #print(maxCounter)
                        maxVals[maxCounter] = maxVals[minCounter] + 1
                        #print(maxVals)
                        maxCounter = 0

                if flipper == -1:
                    if diags[diag][cur] == -1 or (diags[diag][cur] == 0 and minCounter > 0):
                        minCounter += 1
                        #print(minCounter)
                    else:
                        flipper *= -1 
                        #print("flipped")
                        #print(minCounter)
                        minVals[minCounter] = minVals[minCounter] + 1
                        #print(minVals)
                        minCounter = 0

        for i in range(1, len(maxVals)):
            evalRet += diagCoeff*(maxVals[i]-minVals[i])*i    
        #Checks for potential point streaks vertically by seeing if a current chip is boxed off from empty spaces or friendly pieces
        #Max moves increase score, min moves decrease score
        # for col in range(0, len(cols)):
        #     for row in range(0, len(cols[col])):
        #         if cols[col][row] == 1 and row != len(cols[col]) - 1 and (cols[col][row+1] == 0 or cols[col][row+1] == 1):
        #             if (maxStreakC - row + 1) > 3:
        #                 evalRet += colCoeff*(maxStreakC - row + 1)
        #         if cols[col][row] == -1 and row != len(cols[col]) - 1 and (cols[col][row+1] == 0 or cols[col][row+1] == -1):
        #             if (maxStreakC - row + 1) > 3:
        #                 evalRet -= colCoeff*(maxStreakC - row + 1)
            
        # #Checks for potential point streaks horizontally by seeing if a current chip is boxed off from empty spaces or friendly pieces
        # #Max moves increase score, min moves decrease score
        # for row in range(0, len(rows)):
        #     for col in range(0, len(rows[row])):
        #         if rows[row][col] == 1 and col != len(rows[row]) - 1 and (rows[row][col+1] == 0 or rows[row][col+1] == 1):
        #             if (maxStreakR - col + 1) > 3:
        #                 evalRet += rowCoeff*(maxStreakR - row + 1)
        #         if rows[row][col] == -1 and col != len(rows[row]) - 1 and (rows[row][col+1] == 0 or rows[row][col+1] == -1):
        #             if (maxStreakR - col + 1) > 3:
        #                 evalRet -= rowCoeff*(maxStreakR - row + 1)
        print(evalRet)
        return evalRet


class MinimaxHeuristicPruneAgent(MinimaxHeuristicAgent):
    """Smarter computer agent that uses minimax with alpha-beta pruning to select the best move."""

    def minimax(self, state):
        """Determine the minimax utility value the given state using alpha-beta pruning.

        The value should be equal to the one determined by MinimaxAgent.minimax(), but the 
        algorithm should do less work.  You can check this by inspecting the value of the class 
        variable GameState.state_count, which keeps track of how many GameState objects have been 
        created over time.  This agent should also respect the depth limit like HeuristicAgent.

        N.B.: When exploring the game tree and expanding nodes, you must consider the child nodes
        in the order that they are returned by GameState.successors().  That is, you cannot prune
        the state reached by moving to column 4 before you've explored the state reached by a move
        to to column 1.

        Args: 
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """

        return self.alphaBeta(state, 0, -math.inf, math.inf)

    def alphaBeta(self, state, curDepth, a, b): #standard a-b pruning
        if curDepth is self.depth_limit-1:
            return self.evaluation(state)
        elif curDepth < self.depth_limit-1 and state.is_full():
            print("got to terminal")
            return state.utility()
        
        #utilScores = []
        if state.next_player() == 1:
            maximum = -math.inf
            for move, state in state.successors():
                #utilScores.append(self.alphaBeta(state, curDepth + 1, a, b))
                maximum = max(maximum, self.alphaBeta(state, curDepth + 1, a, b))
                a = max(a, maximum)
                if b <= a:
                    break
            return maximum
        else:
            minimum = math.inf
            for move, state in state.successors():
                #utilScores.append(self.alphaBeta(state, curDepth + 1, a, b))
                minimum = min(minimum, self.alphaBeta(state, curDepth + 1, a, b))
                b = min(b, minimum)
                if b <= a:
                    break
            return minimum



