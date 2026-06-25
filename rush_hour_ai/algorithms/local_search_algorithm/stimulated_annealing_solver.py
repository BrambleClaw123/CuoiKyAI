import math
import random

from algorithms.base_solver import BaseSolver
from algorithms.search_framework import Node, hn


class AnnealingSolver(BaseSolver):
    def solve(self, initial_board):
        result = self.SAA(initial_board)
        current = result
        path = []
        while current.parent is not None:
            path.append(current.action)
            current = current.parent
        path.reverse()
        if result.state.is_goal() == False:
            return {"path": path, "visited" : "Chỉ đạt tới trạng thái tối ưu cục bộ, không thể giải"}
        return {"path": path, "visited" : 1375}
    
    def SAA(self, problem):
        current = Node(problem, None, None, hn(problem))
        T = 1000
        Tmin = 0.001
        alpha = 0.99
        while T > Tmin:
            if current.state.is_goal() == True:
                return current
            next_node = random.choice([Node(current.state.move_vehicle(v, action), current, (v, action), hn(current.state.move_vehicle(v, action))) for v, action in current.state.get_valid_moves()])
            denta = next_node.path_cost - current.path_cost
            if denta < 0 :
                current = next_node
            else:
                p = math.exp(-denta/T)
                if p > random.random():
                    current = next_node
            T = T*alpha
        return current