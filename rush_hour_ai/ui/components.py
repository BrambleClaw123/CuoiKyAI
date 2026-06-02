import pygame
from core.constants import *

class Button:
    def __init__(self, x, y, width, height, text, value, bg_color=(46, 134, 193)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.value = value
        self.color = bg_color
        # Làm sáng màu nền lên một chút khi hover
        self.hover_color = (min(bg_color[0]+30, 255), min(bg_color[1]+30, 255), min(bg_color[2]+30, 255))
        self.font = pygame.font.SysFont("segoe ui", 20, bold=True)
        # Khung đổ bóng nằm lệch xuống dưới 4 pixel
        self.shadow_rect = pygame.Rect(x + 2, y + 4, width, height)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        current_color = self.hover_color if is_hover else self.color
        
        # 1. Vẽ bóng đen mờ đằng sau (Nếu đang hover thì bóng nhạt đi)
        shadow_color = (20, 20, 20) if not is_hover else (40, 40, 40)
        pygame.draw.rect(surface, shadow_color, self.shadow_rect, border_radius=10)
        
        # 2. Hiệu ứng nhún: Trồi lên nếu hover
        button_rect = self.rect.move(0, -3) if is_hover else self.rect
        pygame.draw.rect(surface, current_color, button_rect, border_radius=10)
        
        # 3. Vẽ chữ
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=button_rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return self.value
        return None