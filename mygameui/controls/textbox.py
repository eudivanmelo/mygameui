from pygame import Surface, constants, mouse, time
from pygame.event import Event

from .control import Control
import mygameui.utils as ui_utils
import mygameui.globals as ui_globals

class Textbox(Control):
    """
    Representa um controle de caixa de texto que pode ser usado para entrada de texto.

    Parâmetros:
    - x (int): A coordenada x da posição inicial do textbox.
    - y (int): A coordenada y da posição inicial do textbox.
    - width (int): A largura do textbox.
    - height (int): A altura do textbox.
    - text (str): O texto inicial dentro do textbox (opcional).

    Atributos:
    - text (str): O texto atual dentro do textbox.
    - is_password (bool): Indica se o texto deve ser exibido como uma senha.
    - font (Font): A fonte utilizada para renderizar o texto no textbox.
    - font_color ((int, int, int)): A cor do texto no textbox, representada como uma tupla RGB.
    - align (tuple): Ajustes de alinhamento do texto no textbox, no formato (alinhamento, deslocamento).
    """

    def __init__(self, x, y, width, height, text = ''):
        super().__init__(x, y, width, height)

        self._text = ''
        self.font = ui_globals.font
        self.font_color = (255, 255, 255)
        self.align = ('left', 8)

        self._on_changed_text = None
        self.__visible_text = ''
        self.__is_password = False
        self.__select_index = 0
        self.__last_tick = time.get_ticks()
        self.__visible_cursor = True

        self.text = text
        self.set_surface_theme(ui_globals.theme)

    ## ========== Property's ==================

    @property
    def text(self):
        """
        Obtém o texto atual dentro do textbox.

        Retorna:
        str: O texto atual dentro do textbox.
        """
        return self._text
    
    @text.setter
    def text(self, new_text):
        if self._text != new_text:
            self._text = new_text

            if self.is_password:
                self.__visible_text = '*' * len(new_text)
            else:
                self.__visible_text = new_text
            self._call_changed_text()

    @property
    def is_password(self):
        """
        Obtém o estado atual da exibição de senha no textbox.

        Retorna:
        bool: True se o texto está sendo exibido como uma senha, False caso contrário.
        """
        return self.__is_password
    
    @is_password.setter
    def is_password(self, value: bool):
        self.__is_password = value

        if self.__is_password:
            self.__visible_text = '*' * len(self._text)
        else:
            self.__visible_text = self._text

    ## ========== Set Function's ==============

    def set_surface_theme(self, theme: Surface):
        """
        Define o tema visual do textbox.

        Args:
        theme (Surface): A superfície contendo o tema visual do textbox.
        """
        self.__normal_render = ui_utils.generate_surface_byrect(theme.subsurface(96, 16, 16, 16), 
                                                                self.width, self.height)
        self.__active_render = ui_utils.generate_surface_byrect(theme.subsurface(112, 16, 16, 16), 
                                                                self.width, self.height)

    def set_on_changed_text(self, func, args=()):
        """
        Define uma função a ser chamada sempre que o texto dentro do textbox for alterado.

        Args:
        func (function): A função a ser chamada quando o texto for alterado.
        args (tuple): Os argumentos adicionais a serem passados para a função (opcional).
        """
        self._on_changed_text = (func, args)

    ## ========== Call Function's =============

    def _call_changed_text(self):
        """
        Chama a função registrada para ser chamada sempre que o texto dentro do textbox for alterado.
        """
        if self._on_changed_text:
            self._on_changed_text[0](*self._on_changed_text[1])

    ## ========== Private Function's ==========
    
    def _update_render_rect(self):
        super()._update_render_rect()
        
        render = self.font.render(self._text, True, self.font_color)
        if self.align[0] == 'left':
            self.__text_x = self._render_rect.x + self.align[1]
            self.__text_y = self._render_rect.center[1] - render.get_rect().center[1]

        elif self.align[0] == 'center':
            self.__text_x = self._render_rect.center[0] - render.get_rect().center[0]
            self.__text_y = self._render_rect.center[1] - render.get_rect().center[1]

        elif self.align[0] == 'top':
            self.__text_x = self._render_rect.center[0] - render.get_rect().center[0]
            self.__text_y = self._render_rect.center[1] + self.align[1]
        else:
            self.__text_x = self._render_rect.x
            self.__text_y = self._render_rect.y

    ## ========== Public Function's ===========

    def draw(self, screen: Surface):
        if self._active:
            screen.blit(self.__active_render, self._render_rect)
        else:
            screen.blit(self.__normal_render, self._render_rect)

        render = self.font.render(self.__visible_text, True, self.font_color)
        screen.blit(render, (self.__text_x, self.__text_y))

        if self._active and self.__visible_cursor:
            render = self.font.render(self.__visible_text, True, self.font_color)
            screen.blit(self.font.render('|', True, self.font_color), 
                        (self.__text_x + self.font.size(self.__visible_text[:self.__select_index])[0] - 1, self.__text_y))

    def update(self, events: list[Event]):
        super().update(events)

        for event in events:
            if event.type == constants.MOUSEBUTTONDOWN and self._is_hovered:
                if event.button == 1:  # Verifica se o clique foi com o botão esquerdo
                    click_pos = mouse.get_pos()[0] - self.__text_x
                    self.__select_index = 0
                    self.__visible_cursor = True
                    for i in range(len(self.__visible_text)):
                        size = self.font.size(self.__visible_text[:i+1])[0]
                        if click_pos <= size:
                            self.__select_index = i
                            break
                        elif click_pos > size:
                            self.__select_index = len(self.__visible_text)
            elif event.type == constants.KEYDOWN and self._active:
                if event.key == constants.K_BACKSPACE:
                    if self.__select_index > 0:
                        self.text = self._text[:self.__select_index - 1] + self._text[self.__select_index:]
                        self.__select_index -= 1
                else:
                    self.text = self._text[:self.__select_index] + event.unicode + self._text[self.__select_index:]
                    self.__select_index += 1

        # Verifica o tempo para piscar o cursor
        if self._active:
            if time.get_ticks() - self.__last_tick >= 500:
                self.__visible_cursor = not self.__visible_cursor
                self.__last_tick = time.get_ticks()
            
                        