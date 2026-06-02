import os
import random
import pygame
from core.constants import *
from core.game_state import GameState

pygame.font.init()
CAR_FONT = pygame.font.SysFont("segoe ui", 24, bold=True)

ASSETS = {}
# Bộ nhớ tạm: Lưu trữ mẫu xe đã được bốc thăm cho từng ID (Ví dụ: {'A': 0, 'B': 2, 'C': 1})
VEHICLE_VARIANTS = {}

def load_assets():
    if ASSETS: return 
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_dir = os.path.join(base_dir, "assets", "images")
    
    def load_img(filename):
        path = os.path.join(img_dir, filename)
        if os.path.exists(path):
            return pygame.image.load(path).convert_alpha() 
        return None
    
    ASSETS['board_bg'] = load_img("board_bg.jpg")

    # Load xe mục tiêu (chỉ có 1 loại)
    ASSETS['target'] = load_img("main_car.png")
    
    # Load 3 biến thể cho từng chiều dài xe (từ 2 đến 6 ô)
    for length in range(2, 7): 
        ASSETS[f'normal_{length}'] = [] # Tạo một mảng trống để chứa 3 ảnh
        for variant in range(1, 4):     # Chạy từ 1 đến 3
            filename = f"car_{length}_{variant}.png"
            img = load_img(filename)
            if img: # Chỉ thêm vào mảng nếu tải file thành công
                ASSETS[f'normal_{length}'].append(img)

def draw_board(surface, state: GameState, offset_x=20, offset_y=20):
    load_assets()

    # --- 1. VẼ SÀN XE VÀ "DÌM" NHIỄU BẰNG OVERLAY ---
    bg_img = ASSETS.get('board_bg')
    if bg_img:
        tile_img = pygame.transform.scale(bg_img, (CELL_SIZE, CELL_SIZE))
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                tile_x = offset_x + col * CELL_SIZE
                tile_y = offset_y + row * CELL_SIZE
                surface.blit(tile_img, (tile_x, tile_y))
        
        # THỦ THUẬT: Vẽ một tấm màng đen mờ (Alpha) phủ lên trên để giảm độ gắt của nền
        overlay = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
        overlay.set_alpha(160) # 0: Trong suốt -> 255: Đen thui. 160 là dìm nền cực đẹp.
        overlay.fill((15, 15, 20)) # Ám thêm một chút sắc xanh đen cho sang
        surface.blit(overlay, (offset_x, offset_y))
    else:
        pygame.draw.rect(surface, GRID_BG, (offset_x, offset_y, BOARD_SIZE, BOARD_SIZE))

    # --- 2. VẼ KẺ VẠCH ĐƯỜNG MỜ HƠN ---
    # Chỉnh màu vạch kẻ tối lại một chút để không bị chói
    subtle_line = (60, 65, 70)
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(surface, subtle_line, (offset_x + i * CELL_SIZE, offset_y), (offset_x + i * CELL_SIZE, offset_y + BOARD_SIZE), 2)
        pygame.draw.line(surface, subtle_line, (offset_x, offset_y + i * CELL_SIZE), (offset_x + BOARD_SIZE, offset_y + i * CELL_SIZE), 2)

    # Lối thoát (Làm màu đỏ đô cho đỡ gắt)
    exit_y = offset_y + 2 * CELL_SIZE
    exit_x = offset_x + BOARD_SIZE
    pygame.draw.rect(surface, (180, 40, 40), (exit_x, exit_y, 10, CELL_SIZE))

    # --- 3. VẼ XE CÓ BÓNG ĐỔ VÀ PADDING RỘNG HƠN ---
    for v in state.vehicles:
        px = offset_x + v.x * CELL_SIZE
        py = offset_y + v.y * CELL_SIZE
        pwidth = v.length * CELL_SIZE if v.orientation == 'H' else CELL_SIZE
        pheight = CELL_SIZE if v.orientation == 'H' else v.length * CELL_SIZE
            
        # Tăng padding từ 2 lên 6 để xe có không gian "thở", không bị chạm vạch lưới
        pad = 6 
        car_rect = pygame.Rect(px + pad, py + pad, pwidth - 2*pad, pheight - 2*pad)
        
        img = None
        if v.is_target:
            img = ASSETS.get('target')
        else:
            variants = ASSETS.get(f'normal_{v.length}', [])
            if variants:
                if v.id not in VEHICLE_VARIANTS:
                    VEHICLE_VARIANTS[v.id] = random.randint(0, len(variants) - 1)
                img = variants[VEHICLE_VARIANTS[v.id]]
        
        if img:
            if v.orientation == 'H':
                rotated_img = pygame.transform.rotate(img, -90)
                final_img = pygame.transform.scale(rotated_img, (car_rect.width, car_rect.height))
            else: 
                final_img = pygame.transform.scale(img, (car_rect.width, car_rect.height))
            
            # THỦ THUẬT: Vẽ bóng đổ (Drop Shadow) dưới gầm xe
            shadow_rect = car_rect.copy()
            shadow_rect.move_ip(5, 5) # Đẩy bóng xéo xuống góc phải dưới 5 pixel
            pygame.draw.rect(surface, (10, 10, 10), shadow_rect, border_radius=10) # Bóng màu đen xám
            
            # Vẽ hình xe đè lên trên bóng
            surface.blit(final_img, car_rect.topleft)
        else:
            color = RED if v.is_target else BLUE
            # Thêm bóng cho xe dạng khối hộp (Fallback)
            shadow_rect = car_rect.copy()
            shadow_rect.move_ip(4, 4)
            pygame.draw.rect(surface, (20, 20, 20), shadow_rect, border_radius=8)
            pygame.draw.rect(surface, color, car_rect, border_radius=8)
        
        # Vẽ ID lên xe (Giữ nguyên)
        text_surf = CAR_FONT.render(v.id, True, WHITE)
        shadow_surf = CAR_FONT.render(v.id, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=car_rect.center)
        shadow_rect = text_rect.copy()
        shadow_rect.move_ip(2, 2)
        
        surface.blit(shadow_surf, shadow_rect)
        surface.blit(text_surf, text_rect)