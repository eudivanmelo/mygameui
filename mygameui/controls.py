from pygame import Rect, draw as pydraw, mouse, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.surface import Surface
from pygame.event import Event

class Control:
    """
    Classe base para todos os controles da interface do usuário.
    """
    def __init__(self, x, y, width, height):
        """
        Inicializa um controle com sua posição e tamanho.

        Args:
            x (int): Coordenada x da posição do controle.
            y (int): Coordenada y da posição do controle.
            width (int): Largura do controle.
            height (int): Altura do controle.
        """
        self._rect = Rect(x, y, width, height)
        self._render_rect = self._rect
        self._is_hovered = False
        self._is_clicked = False
        self._visible = True
        self._parent: Control = None

        # Função a ser chamada quando o mouse é liberado sobre o controle
        self._on_mouse_up = None

    # ========= Property's =============

    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, control):
        self._parent = control
        self.__update_render_rect()
            
    @property
    def rect(self):
        return self._rect
    
    @property
    def x(self):
        """
        int: Coordenada x da posição do controle.
        """
        return self._rect.x
    
    @x.setter
    def x(self, value):
        self._rect.x = value
        self.__update_render_rect()
    
    @property
    def y(self):
        """
        int: Coordenada y da posição do controle.
        """
        return self._rect.y
    
    @y.setter
    def y(self, value):
        self._rect.y = value
        self.__update_render_rect()
    
    @property
    def position(self):
        """
        tuple: Tupla contendo as coordenadas x e y da posição do controle.
        """
        return (self._rect.x, self._rect.y)
    
    @property
    def width(self):
        """
        int: Largura do controle.
        """
        return self._rect.width
    
    @width.setter
    def width(self, value):
        self._rect.width = value
        self.__update_render_rect()

    @property
    def height(self):
        """
        int: Altura do controle.
        """
        return self._rect.height
    
    @height.setter
    def height(self, value):
        self._rect.height = value
        self.__update_render_rect()

    @property
    def size(self):
        """
        tuple: Tupla contendo a largura e a altura do controle.
        """
        return (self._rect.width, self._rect.height)

    @property
    def visible(self):
        """
        bool: Indica se o controle está visível ou não.
        """
        return self._visible
    
    @visible.setter
    def visible(self, value):
        """
        Define a visibilidade do controle.

        Args:
            value (bool): True se o controle deve ser visível, False caso contrário.
        """
        if self._visible != value:
            self._visible = value
            # Adicionar funcionalidade caso altere a visibilidade

    # ========== Action's ===========

    def set_on_mouse_up(self, func, args=()):
        """
        Define a função a ser chamada quando o mouse é liberado sobre o controle.

        Args:
            func (function): Função a ser chamada.
            args (tuple, optional): Argumentos a serem passados para a função (default é ()).
        """
        self._on_mouse_up = (func, args)

    def _call_on_mouse_up(self):
        """
        Chama a função definida para ser executada quando o mouse é liberado sobre o controle.
        """
        if self._on_mouse_up:
            self._on_mouse_up[0](*self._on_mouse_up[1])

    # ========== Private Function's =========

    def __update_render_rect(self):
        if self._parent:
            self._render_rect = Rect(self._rect.x + self.parent.rect.x,
                                     self._rect.y + self.parent.rect.y,
                                     self._rect.width, self._rect.height)
        else:
            self._render_rect = self._rect

    # ========== Public Function's ============

    def reset(self):
        self._is_hovered = False

    def draw(self, screen: Surface):
        """
        Método abstrato para desenhar o controle.
        """
        pass

    def update(self, events: list[Event]):
        """
        Atualiza o estado do controle com base nos eventos fornecidos.

        Args:
            events (list[Event]): Lista de eventos do pygame.
        """
        if not self._visible:
            return
        
        if self._render_rect.collidepoint(mouse.get_pos()):
            if not self._is_hovered:
                self._is_hovered = True
                # Adicionar funcionalidade para quando o mouse entra no controle
        else:
            if self._is_hovered:
                self._is_hovered = False
                self._is_clicked = False
                # Adicionar funcionalidade para quando o mouse sai do controle

        if self._is_hovered:
            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    if not self._is_clicked:
                        self._is_clicked = True
                        # Adicionar funcionalidade para quando o mouse é pressionado sobre o controle
                elif event.type == MOUSEBUTTONUP:
                    if self._is_clicked:
                        self._is_clicked = False
                        self._call_on_mouse_up()

class Window(Control):
    def __init__(self, x, y, width, height, caption = '', closable = True, movable = True):
        super().__init__(x, y, width, height)
        self.caption = caption
        self.closable = closable # TODO Implementar essa funcionalidade
        self.movable = movable # TODO Implementar essa funcionalidade

        self._controls: list[Control] = []

    def add_control(self, control: Control):
        self._controls.append(control)
        control.parent = self

    def draw(self, screen):
        for control in self._controls:
            control.draw(screen)

    def update(self, events: list[Event]):
        for control in reversed(self._controls):
            control.update(events)
            if control.rect.collidepoint(mouse.get_pos()):
                for c in self._controls:
                    if c != control:
                        c.reset()

                break   

class Button(Control):
    """
    Classe para criar um botão clicável.
    """

    def __init__(self, x, y, width, height, text='', 
                 normal_img=None, 
                 hover_img=None, 
                 click_img=None):
        """
        Inicializa um botão com sua posição, tamanho e imagens.

        Args:
            x (int): Coordenada x da posição do botão.
            y (int): Coordenada y da posição do botão.
            width (int): Largura do botão.
            height (int): Altura do botão.
            text (str, optional): Texto a ser exibido no botão (default é '').
            normal_img (Surface, optional): Imagem a ser exibida quando o botão está no estado normal (default é None).
            hover_img (Surface, optional): Imagem a ser exibida quando o mouse está sobre o botão (default é None).
            click_img (Surface, optional): Imagem a ser exibida quando o botão está sendo clicado (default é None).
        """
        super().__init__(x, y, width, height)
        self.text = text
        self.normal_img = normal_img
        self.hover_img = hover_img
        self.click_img = click_img

    def draw(self, screen: Surface):
        """
        Desenha o botão na tela.

        Args:
            screen (Surface): Superfície onde o botão será desenhado.
        """

        if not self._visible:
            return # Não exibir controle caso não esteja visível
        
        # Definir posição com base na posição do parente
        
        if self._is_hovered:
            if self._is_clicked:
                if self.click_img:
                    screen.blit(self.click_img, self._render_rect)
                else:
                    pydraw.rect(screen, (0, 0, 0), self._render_rect)
            else:
                if self.hover_img:
                    screen.blit(self.hover_img, self._render_rect)
                else:
                    pydraw.rect(screen, (255, 255, 255), self._render_rect)
        else:
            if self.normal_img:
                screen.blit(self.normal_img, self._render_rect)
            else:
                pydraw.rect(screen, (128, 128, 128), self._render_rect)