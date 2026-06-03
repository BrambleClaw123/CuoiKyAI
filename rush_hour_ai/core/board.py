class Board:
    def __init__(self, vehicles, bricks=None):
        self.vehicles = {v.name: v for v in vehicles}
        # Lưu danh sách tọa độ gạch cố định dưới dạng tập hợp các tuple: {(row, col), ...}
        self.bricks = set(bricks) if bricks else set()

    def get_occupied_cells(self):
        occupied = {}
        
        # 1. Đánh dấu các ô bị chiếm bởi xe
        for name, v in self.vehicles.items():
            for i in range(v.size):
                r = v.row + (i if v.orientation == 'V' else 0)
                c = v.col + (i if v.orientation == 'H' else 0)
                occupied[(r, c)] = name
                
        # 2. Đánh dấu các ô bị chiếm bởi gạch cố định (gọi tên ký hiệu chung là 'BRICK')
        for (r, c) in self.bricks:
            occupied[(r, c)] = 'BRICK'
            
        return occupied

    def is_goal(self):
        return self.vehicles['X'].col == 4

    def state_key(self):
        # Vì gạch cố định không bao giờ di chuyển nên key trạng thái chỉ cần lưu vị trí xe là đủ
        return tuple(sorted((name, v.row, v.col) for name, v in self.vehicles.items()))

    def get_valid_moves(self):
        moves = []
        occupied = self.get_occupied_cells()

        for name, v in self.vehicles.items():
            if v.orientation == 'H':
                if v.col > 0 and (v.row, v.col - 1) not in occupied:
                    moves.append((name, -1))
                if v.col + v.size < 6 and (v.row, v.col + v.size) not in occupied:
                    moves.append((name, 1))
            elif v.orientation == 'V':
                if v.row > 0 and (v.row - 1, v.col) not in occupied:
                    moves.append((name, -1))
                if v.row + v.size < 6 and (v.row + v.size, v.col) not in occupied:
                    moves.append((name, 1))
        return moves

    def move_vehicle(self, name, steps):
        new_vehicles = [v.clone() for v in self.vehicles.values()]
        # Truyền lại danh sách gạch cũ sang trạng thái Board mới
        new_board = Board(new_vehicles, self.bricks)
        target_v = new_board.vehicles[name]
        if target_v.orientation == 'H':
            target_v.col += steps
        else:
            target_v.row += steps
        return new_board