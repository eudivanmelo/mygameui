from pygame import Rect, Surface, transform, constants, mouse
from pygame.event import Event

from .control import Control
from .button import Button
import mygameui.globals as ui_globals

class Form(Control):
    """A classe Form representa uma janela de formulário na interface do usuário.

    Attributes:
        x (int): A coordenada x do canto superior esquerdo do formulário.
        y (int): A coordenada y do canto superior esquerdo do formulário.
        width (int): A largura do formulário.
        height (int): A altura do formulário.
        caption (str): O texto exibido como título do formulário.
        caption_color (tuple): A cor do texto do título.
        closable (bool): Indica se o formulário possui botão de fechar.
        movable (bool): Indica se o formulário pode ser movido.

    Methods:
        set_surface_theme(theme): Define a aparência do formulário com base em um tema.
        set_surface_image(image: Surface): Define a imagem do formulário manualmente.
        draw(screen): Desenha o formulário na tela especificada.
        update(events: list[Event]): Atualiza o formulário com base nos eventos recebidos.
    """

    def __init__(self, x, y, width, height, caption = '', closable = True, movable = True):
        super().__init__(x, y, width, height)

        self.caption = caption
        self.caption_color = (200, 200, 200)
        self.closable = closable
        self.movable = movable
        self.movable_rect = Rect(x, y, width, 16)
        self.__moving = False

        self.set_surface_theme(ui_globals.theme)

    # ========== Property's ============

    @property
    def closable(self):
        return self.__closable
    
    @closable.setter
    def closable(self, value: bool):
        """Define se o formulário possui um botão de fechar.

        Args:
            value (bool): Valor indicando se o formulário é fechável.
        """
        self.__closable = value
        if value == True:
            self.__close_button = Button(self.width - 16, 0, 16, 16)
            self.__close_button.set_on_mouse_up(lambda: setattr(self, 'visible', False))
            self.add_control(self.__close_button)

    # ======== Set Function's ===========

    def set_surface_theme(self, theme):
        """Define a aparência do formulário com base em um tema.

        Args:
            theme: O tema que contém os elementos de estilo do formulário.

        """
        width = self._rect.width
        height = self._rect.height
        self.__render = Surface((self.width, self.height)).convert_alpha()
        self.__render.fill((0,0,0,0))

        ## ===== TOP =======
        if self.movable:
            # Canto superior esquerdo
            render_left_top = theme.subsurface(48, 0, 16, 16)
            # Centro superior
            render_middle_top = transform.scale(theme.subsurface(64, 0, 16, 16), (width - 32, 16))
            # Canto superior direito
            render_right_top = theme.subsurface(80, 0, 16, 16)
        else:
            # Canto superior esquerdo
            render_left_top = theme.subsurface(0, 0, 16, 16)
            # Centro superior
            render_middle_top = transform.scale(theme.subsurface(16, 0, 16, 16), (width - 32, 16))
            # Canto superior direito
            render_right_top = theme.subsurface(32, 0, 16, 16)

        self.__render.blit(render_left_top, (0, 0))
        self.__render.blit(render_middle_top, (16, 0))
        self.__render.blit(render_right_top, (width - 16, 0))
        
        ## ===== MIDDLE =======
        # Canto meio esquerdo
        render_left_middle = transform.scale(theme.subsurface(0, 16, 16, 16), (16, height - 32))
        self.__render.blit(render_left_middle, (0, 16))
        
        # Centro meio
        self.__render_middle_middle = transform.scale(theme.subsurface(16, 16, 16, 16), (width - 32, height - 32))
        self.__render.blit(self.__render_middle_middle, (16, 16))
            
        # Canto meio direito
        self.__render_right_middle = transform.scale(theme.subsurface(32, 16, 16, 16), (16, height - 32))
        self.__render.blit(self.__render_right_middle, (width - 16, 16))

        ## ===== BOTTOM =======
        # Canto inferior esquerdo
        render_left_bottom = theme.subsurface(0, 32, 16, 16)
        self.__render.blit(render_left_bottom, (0, height - 16))
            
        # Centro inferior
        render_middle_bottom = transform.scale(theme.subsurface(16, 32, 16, 16), (width - 32, 16))
        self.__render.blit(render_middle_bottom, (16, height - 16))
            
        # Canto inferior direito
        render_right_bottom = theme.subsurface(32, 32, 16, 16)
        self.__render.blit(render_right_bottom, (width - 16, height - 16))

        # Configurar botão de fechar
        if self.closable and self.__close_button:
            self.__close_button.normal_img = theme.subsurface(96, 0, 16, 16)
            self.__close_button.click_img = theme.subsurface(96, 0, 16, 16)
            self.__close_button.hover_img = theme.subsurface(112, 0, 16, 16)

    def set_surface_image(self, image: Surface):
        """Define a imagem do formulário manualmente.

        Args:
            image (Surface): A imagem a ser usada como aparência do formulário.
        """
        self.__render = image

    # ======== Public Function's ========

    def draw(self, screen):
        if not self.visible:
            return # Não mostrar controle caso ele não esteja visível
        
        x = self._rect.x
        y = self._rect.y
        
        if self.__render:
            screen.blit(self.__render, (x, y))

        # Desenhar o texto
        if len(self.caption) > 0:
            screen.blit(ui_globals.font.render(self.caption, True, self.caption_color), (x + 8, y + 3))

        # Render controls in order
        for control in self._controls:
            control.draw(screen)

    def update(self, events: list[Event]):
        if not self.visible:
            return # Não atualizar controle caso ele não esteja visível
        
        if self.movable:
            for event in events:
                if event.type == constants.MOUSEBUTTONDOWN and event.button == 1:
                    if self.movable_rect.collidepoint(mouse.get_pos()):
                        self.__moving = True
                elif event.type == constants.MOUSEBUTTONUP:
                    self.__moving = False
                elif event.type == constants.MOUSEMOTION:
                    if self.__moving:
                        self.move_ip(event.rel)
                        self.movable_rect.move_ip(event.rel)

        for control in reversed(self._controls):
            control.update(events)
            if control.rect.collidepoint(mouse.get_pos()):
                for c in self._controls:
                    if c != control:
                        c.reset()

                break   
