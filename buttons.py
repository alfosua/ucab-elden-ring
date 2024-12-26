
from pygame import Vector2, Color, Surface
from pygame.font import Font
from pygame.rect import Rect
from transform_utils import gaussian_blur


class TextButton:
    def __init__(self, text: str, font: Font, color_base: Color, color_selected: Color, position: Vector2, anchor: Vector2):
        self.selected = False
        self.drawable_base = font.render(text, False, color_base)
        self.drawable_selected = font.render(text, False, color_selected)
        self.drawable_blur = gaussian_blur(self.drawable_base, 5)
        self.drawable_rect = self.drawable_base.get_rect()
        self.drawable_size = Vector2(self.drawable_rect.size)
        self.anchor_offset = Vector2(self.drawable_size.x * anchor.x, self.drawable_size.y * anchor.y)
        self.draw_rect = Rect(position - self.anchor_offset, self.drawable_size)

    def draw(self, surface: Surface):
        if self.selected:
            surface.blit(self.drawable_blur, self.draw_rect.topleft)
        target_drawable = self.drawable_base if not self.selected else self.drawable_selected
        surface.blit(target_drawable, self.draw_rect.topleft)
