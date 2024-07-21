from pygame import Surface

from .control import Control
import mygameui.globals as ui_globals

class CheckBox(Control):
    def __init__(self, x, y, value = False, text = ''):
        super().__init__(x, y, 16, 16)

        self.__value : bool = value

        self.text = text
        self.font = ui_globals.font
        self.font_color = (255,255,255)

        self._on_changed_value = None

        self.set_surface_theme(ui_globals.theme)

    ## ========== Property's ==================

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if self.__value != value:
            self.__value = value
            self._call_changed_value()

    ## ========== Set Function's ==============

    def set_surface_theme(self, theme: Surface):
        self.__normal_render = theme.subsurface(48, 32, 16, 16)
        self.__hover_render = theme.subsurface(64, 32, 16, 16)
        self.__checked_render = theme.subsurface(80, 32, 16, 16)

    def set_on_changed_value(self, func, args=()):
        self._on_changed_value = (func, args)

    ## ========== Call Function's =============

    def _call_changed_value(self):
        if self._on_changed_value:
            self._on_changed_value[0](*self._on_changed_value[1])

    def _call_on_mouse_down(self):
        self.value = not self.value

        super()._call_on_mouse_down()
    ## ========== Public Function's ===========

    def draw(self, screen: Surface):
        if self._is_hovered:
            screen.blit(self.__hover_render, self._render_rect)
        else:
            screen.blit(self.__normal_render, self._render_rect)

        if self.value:
            screen.blit(self.__checked_render, self._render_rect)

        if len(self.text) > 0:
            render = self.font.render(self.text, True, self.font_color)
            screen.blit(render, (self._render_rect.x + 18, self._render_rect.centery - render.get_rect().centery + 1))