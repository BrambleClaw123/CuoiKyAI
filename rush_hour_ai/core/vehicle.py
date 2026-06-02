class Vehicle:
    def __init__(self, id: str, x: int, y: int, length: int, orientation: str, is_target: bool = False):
        self.id = id
        self.x = x
        self.y = y
        self.length = length
        self.orientation = orientation  # 'H' hoặc 'V'
        self.is_target = is_target

    def __hash__(self):
        # Tạo mã băm dựa trên các thuộc tính cấu thành vị trí xe
        return hash((self.id, self.x, self.y, self.length, self.orientation))

    def __eq__(self, other):
        if not isinstance(other, Vehicle):
            return False
        return (self.id == other.id and 
                self.x == other.x and 
                self.y == other.y)

    def copy_with_move(self, new_x: int, new_y: int):
        """Tạo ra một bản sao của xe ở vị trí mới (giữ tính bất biến)"""
        return Vehicle(self.id, new_x, new_y, self.length, self.orientation, self.is_target)