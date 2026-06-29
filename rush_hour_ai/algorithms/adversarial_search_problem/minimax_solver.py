from algorithms.base_solver import BaseSolver
import math

class MinimaxSolver(BaseSolver):
    def __init__(self):
        self.MAX_FACTION = ['X', 'A', 'B']
        self.MIN_FACTION = ['C', 'D', 'E']
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
            best_move = self.minimax_decision(current_state, depth=3, is_max_turn=is_max)
            if not best_move:
                break 
            path.append(best_move)
            current_state = current_state.move_vehicle(best_move[0], best_move[1])
        return {"path": path, "visited": self.visited_states}

    def minimax_decision(self, state, depth, is_max_turn):
        best_move = None
        if is_max_turn:
            max_eval = -math.inf
            for move in self.get_faction_moves(state, is_max=True):
                child = state.move_vehicle(move[0], move[1])
                eval_score = self.min_value(child, depth - 1)    
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
        else:
            min_eval = math.inf
            for move in self.get_faction_moves(state, is_max=False):
                child = state.move_vehicle(move[0], move[1])
                eval_score = self.max_value(child, depth - 1)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
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
            v = max(v, self.min_value(child, depth - 1))
        return v

    def min_value(self, state, depth):
        self.visited_states += 1
        if state.is_goal():
            return 1000 + depth
        if depth == 0:
            return self.evaluate(state) 
        valid_moves = self.get_faction_moves(state, is_max=False)
        if not valid_moves:
            return 1000
        v = math.inf
        for move in valid_moves:
            child = state.move_vehicle(move[0], move[1])
            v = min(v, self.max_value(child, depth - 1))
        return v

    def get_faction_moves(self, state, is_max):
        moves = state.get_valid_moves()
        if is_max:
            return [m for m in moves if m[0] not in self.MIN_FACTION]
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
                    weight = 2 if name in self.MIN_FACTION else 1
                    blocking_cars += weight
        max_moves = len(self.get_faction_moves(state, is_max=True))
        min_moves = len(self.get_faction_moves(state, is_max=False))
        return (max_moves - min_moves) - (distance * 10) - (blocking_cars * 20)