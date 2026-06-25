import random
import copy
from algorithms.base_solver import BaseSolver

class MinConflictsSolver(BaseSolver):

    def solve(self, initial_board):
        vehicles_to_place = [
            v for v in initial_board.vehicles.values()
            if v.name != 'X'
        ]
        csp = {
            'variables': [v.name for v in vehicles_to_place],
            'domains': {},
            'board': initial_board
        }
        for v in vehicles_to_place:
            valid_positions = []
            for r in range(6):
                for c in range(6):
                    if v.orientation == 'H' and c + v.size <= 6:
                        valid_positions.append((r, c))
                    elif v.orientation == 'V' and r + v.size <= 6:
                        valid_positions.append((r, c))
            csp['domains'][v.name] = valid_positions
        self.explored_states = []
        solution = self.min_conflicts(csp)
        if solution is None:
            return {"path": self.explored_states, "visited": len(self.explored_states), "solution": None}
        return {"path": self.explored_states, "visited": len(self.explored_states), "solution": solution}
    
    def min_conflicts(self, csp, max_steps=1000):
        current = self.initial_assignment(csp)
        self.explored_states.append(copy.deepcopy(current))
        for _ in range(max_steps):
            if self.is_solution(current, csp):
                return current
            conflicted_vars = self.conflicted_variables(current, csp)
            if not conflicted_vars:
                return current
            var = random.choice(conflicted_vars)
            min_conflict = float('inf')
            best_values = []
            for value in csp['domains'][var]:
                score = self.conflicts(var, value, current, csp)
                if score < min_conflict:
                    min_conflict = score
                    best_values = [value]
                elif score == min_conflict:
                    best_values.append(value)
            current[var] = random.choice(best_values)
            self.explored_states.append(copy.deepcopy(current))
        return None

    def initial_assignment(self, csp):
        assignment = {}
        for var in csp['variables']:
            assignment[var] = random.choice(
                csp['domains'][var]
            )
        return assignment
    
    def is_solution(self, assignment, csp):
        for var in csp['variables']:
            if self.conflicts(var, assignment[var], assignment, csp) > 0:
                return False
        return True

    def conflicted_variables(self, assignment, csp):
        result = []
        for var in csp['variables']:
            if self.conflicts(var, assignment[var], assignment, csp) > 0:
                result.append(var)
        return result

    def conflicts(self, var, value, assignment, csp):
        board = csp['board']
        r, c = value
        vehicle = board.vehicles[var]
        cells = set()
        for i in range(vehicle.size):
            if vehicle.orientation == 'H':
                cells.add((r, c + i))
            else:
                cells.add((r + i, c))
        conflict_count = 0
        for cell in cells:
            if cell in board.bricks:
                conflict_count += 1
        for cell in cells:
            if cell[0] == 2:
                conflict_count += 1
        for other_var, other_value in assignment.items():
            if other_var == var:
                continue
            other_vehicle = board.vehicles[other_var]
            orow, ocol = other_value
            other_cells = set()
            for i in range(other_vehicle.size):
                if other_vehicle.orientation == 'H':
                    other_cells.add((orow, ocol + i))
                else:
                    other_cells.add((orow + i, ocol))
            if not cells.isdisjoint(other_cells):
                conflict_count += 1
        return conflict_count