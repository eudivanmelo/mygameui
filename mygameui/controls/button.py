from pygame import Surface, draw as pg_draw

from .control import Control
import mygameui.globals as ui_globals
import mygameui.utils as ui_utils

class Button(Control):
    """A classe Button representa um botão clicável em uma interface de usuário.

    Attributes:
        x (int): A coordenada x do canto superior esquerdo do botão.
        y (int): A coordenada y do canto superior esquerdo do botão.
        width (int): A largura do botão.
        height (int): A altura do botão.
        text (str): O texto exibido no botão.

    Methods:
        set_surface_theme(theme: Surface): Define a aparência do botão com base em um tema Surface.
        draw(screen: Surface): Desenha o botão na tela especificada.
    """

    def __init__(self, x, y, width, height, text=''):
        super().__init__(x, y, width, height)

        self.text = text
        self.font = ui_globals.font
        self.text_color = (255, 255, 255)

        self.set_surface_theme(ui_globals.theme)

    # ========== Set Function's ============

    def set_surface_theme(self, theme: Surface):
        """Define a aparência do botão com base em um tema Surface.

        Args:
            theme (Surface): O tema Surface que contém os elementos de estilo do botão.

        """
        # Criar imagens para diferentes estados do botão (normal, hover, clique)
        self.normal_img = ui_utils.generate_surface_byrect(theme.subsurface(48, 16, 16, 16), 
                                                        self.width, self.height)
        self.hover_img = ui_utils.generate_surface_byrect(theme.subsurface(64, 16, 16, 16), 
                                                        self.width, self.height)
        self.click_img = ui_utils.generate_surface_byrect(theme.subsurface(80, 16, 16, 16), 
                                                        self.width, self.height)

    # ========= Public Function's

    def draw(self, screen: Surface):
        if not self._visible:
            return # Não exibir controle caso não esteja visível

        if self._is_hovered:
            if self._is_clicked:
                screen.blit(self.click_img, self._render_rect)
            else:
                screen.blit(self.hover_img, self._render_rect)
        else:
            screen.blit(self.normal_img, self._render_rect)

        # Desenhar o texto
        if len(self.text) > 0:
            render = self.font.render(self.text, True, self.text_color)
            text_x = self._render_rect.center[0] - render.get_rect().center[0]
            if self._is_clicked:
                text_y = self._render_rect.center[1] - render.get_rect().center[1]
            else:
                text_y = self._render_rect.center[1] - render.get_rect().center[1] - 1
            screen.blit(render, (text_x, text_y))