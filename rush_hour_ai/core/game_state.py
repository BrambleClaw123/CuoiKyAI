from typing import Tuple
from core.vehicle import Vehicle

class GameState:
    def __init__(self, grid_size: int, vehicles: Tuple[Vehicle, ...]):
        self.grid_size = grid_size
        self.vehicles = vehicles

    def __hash__(self):
        # Băm toàn bộ tuple xe (tuple vốn đã immutable)
        return hash(self.vehicles)

    def __eq__(self, other):
        if not isinstance(other, GameState):
            return False
        return set(self.vehicles) == set(other.vehicles)

    def get_board(self) -> list:
        """Tạo ma trận 2D đại diện cho lưới để in ra console hoặc check va chạm"""
        board = [['.' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for v in self.vehicles:
            for i in range(v.length):
                if v.orientation == 'H':
                    board[v.y][v.x + i] = v.id
                else: # 'V'
                    board[v.y + i][v.x] = v.id
        return board

    def is_goal(self) -> bool:
        """Kiểm tra xem xe mục tiêu (X) đã chạm đến mép phải của bàn cờ chưa"""
        for v in self.vehicles:
            if v.is_target:
                # Nếu phần đuôi của xe chạm mép phải lưới (index = grid_size - 1)
                return v.x + v.length == self.grid_size
        return False

    def get_successors(self):
        successors = []
        # Lấy ma trận 2D hiện tại để dễ dàng check va chạm (ô trống là '.')
        board = self.get_board()

        for i, v in enumerate(self.vehicles):
            if v.orientation == 'H':
                # 1. Kiểm tra xe có thể lùi sang TRÁI (x - 1) không?
                # Điều kiện: x > 0 (chưa đụng tường trái) VÀ ô bên trái là ô trống '.'
                if v.x > 0 and board[v.y][v.x - 1] == '.':
                    new_v = v.copy_with_move(v.x - 1, v.y)
                    new_vehicles = list(self.vehicles)
                    new_vehicles[i] = new_v
                    successors.append(GameState(self.grid_size, tuple(new_vehicles)))
                
                # 2. Kiểm tra xe có thể tiến sang PHẢI (x + 1) không?
                # Điều kiện: Đuôi xe chưa đụng tường phải VÀ ô sát đuôi xe là ô trống '.'
                if v.x + v.length < self.grid_size and board[v.y][v.x + v.length] == '.':
                    new_v = v.copy_with_move(v.x + 1, v.y)
                    new_vehicles = list(self.vehicles)
                    new_vehicles[i] = new_v
                    successors.append(GameState(self.grid_size, tuple(new_vehicles)))

            elif v.orientation == 'V':
                # 3. Kiểm tra xe có thể lùi lên TRÊN (y - 1) không?
                if v.y > 0 and board[v.y - 1][v.x] == '.':
                    new_v = v.copy_with_move(v.x, v.y - 1)
                    new_vehicles = list(self.vehicles)
                    new_vehicles[i] = new_v
                    successors.append(GameState(self.grid_size, tuple(new_vehicles)))

                # 4. Kiểm tra xe có thể tiến xuống DƯỚI (y + 1) không?
                if v.y + v.length < self.grid_size and board[v.y + v.length][v.x] == '.':
                    new_v = v.copy_with_move(v.x, v.y + 1)
                    new_vehicles = list(self.vehicles)
                    new_vehicles[i] = new_v
                    successors.append(GameState(self.grid_size, tuple(new_vehicles)))

        return successors