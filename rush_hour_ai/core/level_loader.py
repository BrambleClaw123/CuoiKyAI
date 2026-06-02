import json

from core.game_state import GameState
from core.vehicle import Vehicle


def load_level(filepath: str) -> GameState:
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    grid_size = data['grid_size']
    vehicles_list = []
    
    for v_data in data['vehicles']:
        vehicle = Vehicle(
            id=v_data['id'],
            x=v_data['x'],
            y=v_data['y'],
            length=v_data['length'],
            orientation=v_data['orientation'],
            is_target=v_data.get('is_target', False)
        )
        vehicles_list.append(vehicle)
        
    # Ép kiểu list thành tuple để đảm bảo tính immutable cho GameState
    return GameState(grid_size, tuple(vehicles_list))