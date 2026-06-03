from algorithms.base_solver import BaseSolver

class DFSSolver(BaseSolver):
    def solve(self, initial_board):
        # Sử dụng cấu trúc dữ liệu Stack (LIFO) cho DFS
        stack = [(initial_board, [])]
        visited = {initial_board.state_key()}
        visited_count = 1

        while stack:
            current_board, path = stack.pop()

            if current_board.is_goal():
                return {"path": path, "visited": visited_count}

            for name, steps in current_board.get_valid_moves():
                next_board = current_board.move_vehicle(name, steps)
                state = next_board.state_key()

                if state not in visited:
                    visited.add(state)
                    visited_count += 1
                    stack.append((next_board, path + [(name, steps)]))
        return None