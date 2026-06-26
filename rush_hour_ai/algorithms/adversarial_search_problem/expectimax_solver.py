from algorithms.base_solver import BaseSolver
import math
import random

class ExpectimaxSolver(BaseSolver):
    def __init__(self):
        self.MAX_FACTION = ['X', 'A', 'B']
        self.CHANCE_FACTION = ['C', 'D', 'E']
        self.max_turns = 20
        self.visited_states = 0

    def solve(self, initial_board):
        self.visited_states = 0
        path = []
        current_state = initial_board
        for turn in range(self.max_turns):
            if current_state.is_goal():
                break 
            is_max = (turn % 2 == 0) 
            best_move = self.expectimax_decision(current_state, depth=3, is_max_turn=is_max)
            if not best_move:
                break
            path.append(best_move)
            current_state = current_state.move_vehicle(best_move[0], best_move[1])

        return {"path": path, "visited": self.visited_states}

    def expectimax_decision(self, state, depth, is_max_turn):
        best_move = None
        if is_max_turn:
            max_eval = -math.inf
            for move in self.get_faction_moves(state, is_max=True):
                child = state.move_vehicle(move[0], move[1])
                eval_score = self.exp_value(child, depth - 1)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
        else:
            valid_moves = self.get_faction_moves(state, is_max=False)
            if valid_moves:
                best_move = random.choice(valid_moves)
        return best_move

    def max_value(self, state, depth):
        self.visited_states += 1
        if state.is_goal():
            return 1000 + depth
        if depth == 0:
            return self.evaluate(state)
        valid_moves = self.get_faction_moves(state, is_max=True)
        if not valid_moves:
            return -1000
        v = -math.inf
        for move in valid_moves:
            child = state.move_vehicle(move[0], move[1])
            v = max(v, self.exp_value(child, depth - 1))
        return v

    def exp_value(self, state, depth):
        self.visited_states += 1
        if state.is_goal():
            return 1000 + depth
        if depth == 0:
            return self.evaluate(state)
        valid_moves = self.get_faction_moves(state, is_max=False)
        if not valid_moves:
            return 1000 
        total = 0
        for move in valid_moves:
            child = state.move_vehicle(move[0], move[1])
            total += self.max_value(child, depth - 1)
        probability = 1 / len(valid_moves)
        return total * probability
    
    def get_faction_moves(self, state, is_max):
        moves = state.get_valid_moves()
        if is_max:
            return [m for m in moves if m[0] not in self.CHANCE_FACTION]
        else:
            return [m for m in moves if m[0] not in self.MAX_FACTION]
        
    def evaluate(self, state):
        if state.is_goal():
            return 1000
        v_x = state.vehicles['X']
        distance = 4 - v_x.col
        blocking_cars = 0
        occupied = state.get_occupied_cells()
        for c in range(v_x.col + v_x.size, 6):
            if (v_x.row, c) in occupied:
                name = occupied[(v_x.row, c)]
                if name != 'BRICK':
                    weight = 2 if name in self.CHANCE_FACTION else 1
                    blocking_cars += weight
        max_moves = len(self.get_faction_moves(state, is_max=True))
        chance_moves = len(self.get_faction_moves(state, is_max=False))
        return (max_moves - chance_moves) - (distance * 10) - (blocking_cars * 20)