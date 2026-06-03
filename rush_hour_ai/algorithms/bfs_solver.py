from collections import deque
from algorithms.base_solver import BaseSolver

class BFSSolver(BaseSolver):
    def solve(self, initial_board):
        queue = deque([(initial_board, [])])
        visited = {initial_board.state_key()}
        visited_count = 1

        while queue:
            current_board, path = queue.popleft()

            if current_board.is_goal():
                return {"path": path, "visited": visited_count}

            for name, steps in current_board.get_valid_moves():
                next_board = current_board.move_vehicle(name, steps)
                state = next_board.state_key()

                if state not in visited:
                    visited.add(state)
                    visited_count += 1
                    queue.append((next_board, path + [(name, steps)]))
        return None