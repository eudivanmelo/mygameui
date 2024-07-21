from pygame import Surface

from .control import Control
import mygameui.globals as ui_globals

class Label(Control):
    def __init__(self, x, y, text):
        super().__init__(x, y, 0, 0)

        self.text = text
        self.font = ui_globals.font
        self.font_color = (255, 255, 255)
        self.background = None

    def draw(self, screen: Surface):
        screen.blit(self.font.render(self.text, True, self.font_color, self.background), self._render_rect)
