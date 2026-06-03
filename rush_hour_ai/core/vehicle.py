class Vehicle:
    def __init__(self, name, row, col, size, orientation, is_target=False):
        self.name = name          
        self.row = row            # Vị trí Y (0 -> 5)
        self.col = col            # Vị trí X (0 -> 5)
        self.size = size          # Độ dài xe
        self.orientation = orientation  # 'H' hoặc 'V'
        self.is_target = is_target

    def clone(self):
        return Vehicle(self.name, self.row, self.col, self.size, self.orientation, self.is_target)