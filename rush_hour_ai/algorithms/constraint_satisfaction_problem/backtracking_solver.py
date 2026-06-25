import copy
from algorithms.base_solver import BaseSolver

class BacktrackingSolver(BaseSolver):
    def solve(self, initial_board):
        vehicles_to_place = [v for v in initial_board.vehicles.values() if v.name != 'X']
        
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
        
        solution = self.backtrack({}, csp)
        
        if solution is not None:
            return {"path": self.explored_states, "visited": len(self.explored_states), "solution": solution}
        return {"path": self.explored_states, "visited": len(self.explored_states), "solution": None}

    def backtrack(self, assignment, csp):
        self.explored_states.append(copy.deepcopy(assignment))
        
        if len(assignment) == len(csp['variables']):
            return assignment
            
        var = self.select_unassigned_variable(assignment, csp)
        
        for value in self.order_domain_values(var, assignment, csp):
            
            if self.is_consistent(var, value, assignment, csp):
                
                assignment[var] = value
                
                result = self.backtrack(assignment, csp)
                
                if result is not None:
                    return result
                    
                del assignment[var]
                self.explored_states.append(copy.deepcopy(assignment))
                
        return None

    def select_unassigned_variable(self, assignment, csp):
        for var in csp['variables']:
            if var not in assignment:
                return var
        return None

    def order_domain_values(self, var, assignment, csp):
        return csp['domains'][var]

    def is_consistent(self, var, value, assignment, csp):
        r, c = value
        board = csp['board']
        v_size = board.vehicles[var].size
        v_orient = board.vehicles[var].orientation
        
        # Tính toán các ô mà xe var sẽ chiếm
        cells = set()
        for i in range(v_size):
            if v_orient == 'H':
                cells.add((r, c + i))
            else:
                cells.add((r + i, c))
                
        # Ràng buộc 1: Không đè lên gạch
        for cell in cells:
            if cell in board.bricks:
                return False
                
        # Ràng buộc 2: Cấm xâm phạm hàng 2 (Đường ra của xe X)
        for cell in cells:
            if cell[0] == 2: 
                return False
                
        # Ràng buộc 3: Không đè lên các xe đã được gán trước đó
        for assigned_var, assigned_val in assignment.items():
            ar, ac = assigned_val
            av_size = board.vehicles[assigned_var].size
            av_orient = board.vehicles[assigned_var].orientation
            for i in range(av_size):
                if av_orient == 'H':
                    if (ar, ac + i) in cells: return False
                else:
                    if (ar + i, ac) in cells: return False
        return True