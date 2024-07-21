from pygame import Rect, mouse
from pygame import constants
from pygame.surface import Surface
from pygame.event import Event

class Control:
    """A classe base para todos os controles na interface do usuário.

    Attributes:
        x (int): A coordenada x do canto superior esquerdo do controle.
        y (int): A coordenada y do canto superior esquerdo do controle.
        width (int): A largura do controle.
        height (int): A altura do controle.
        parent (Control): O controle pai deste controle, se houver.
        rect (Rect): O retângulo de posição e tamanho deste controle.
        visible (bool): Indica se o controle está visível ou não.
        active (bool): Indica se o controle está ativo ou não.

    Methods:
        set_active(value: bool): Define se o controle está ativo ou não.
        set_on_mouse_up(func, args=()): Define a função a ser chamada quando o mouse é liberado sobre o controle.
        set_on_mouse_down(func, args=()): Define a função a ser chamada quando o mouse é pressionado sobre o controle.
        set_surface_theme(theme: Surface): Define a aparência do controle com base em um tema.
        add_control(control): Adiciona um controle a este controle.
        move_ip(pos_relative): Move o controle relativamente à sua posição atual.
        reset(): Reseta o estado do controle.
        draw(screen: Surface): Desenha o controle na tela especificada.
        update(events: list[Event]): Atualiza o estado do controle com base nos eventos fornecidos.

    """

    def __init__(self, x, y, width, height):
        self._rect = Rect(x, y, width, height)
        self._render_rect = self._rect
        self._is_hovered = False
        self._is_clicked = False
        self._visible = True
        self._parent: Control = None
        self._active = False
        self._controls: list[Control] = []

        # Função a ser chamada quando o mouse é liberado sobre o controle
        self._on_mouse_up = None
        self._on_mouse_down = None
        self._on_actived = None

    # ========= Property's =============

    @property
    def parent(self):
        """
        Controle pai deste controle.

        Returns:
            Control: O controle pai deste controle.
        """
        return self._parent
    
    @parent.setter
    def parent(self, control):
        self._parent = control
        self._update_render_rect()
            
    @property
    def rect(self):
        """
        Getter para o retângulo de posição e tamanho deste controle.

        Returns:
            Rect: O retângulo de posição e tamanho deste controle.
        """
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
        self._update_render_rect()
    
    @property
    def y(self):
        """
        int: Coordenada y da posição do controle.
        """
        return self._rect.y
    
    @y.setter
    def y(self, value):
        self._rect.y = value
        self._update_render_rect()
    
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
        self._update_render_rect()

    @property
    def height(self):
        """
        int: Altura do controle.
        """
        return self._rect.height
    
    @height.setter
    def height(self, value):
        self._rect.height = value
        self._update_render_rect()

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

    # ========== Set Function's ===========

    def set_active(self, value: bool):
        """Define se o controle está ativo ou não.

        Quando um controle é ativado, ele é trazido para frente em relação aos outros controles 
        no mesmo nível hierárquico e qualquer controle ativo anteriormente é desativado.

        Args:
            value (bool): True para ativar o controle, False para desativá-lo.
        """
        if value:
            if self.parent:
                self.parent.set_active(True)

                for control in self.parent._controls:
                    control.set_active(False)
                    
                # Bring to the front
                self.parent._controls.remove(self)
                self.parent._controls.append(self)

            self._call_actived()
        else:
            for control in self._controls:
                control.set_active(False)

        self._active = value
    
    def set_on_mouse_up(self, func, args=()):
        """Define a função a ser chamada quando o mouse é liberado sobre o controle.

        Args:
            func: A função a ser chamada quando o mouse é liberado.
            args (tuple, optional): Argumentos adicionais a serem passados para a função. Default é ().

        """
        self._on_mouse_up = (func, args)

    def set_on_mouse_down(self, func, args=()):
        """Define a função a ser chamada quando o mouse é pressionado sobre o controle.

        Args:
            func: A função a ser chamada quando o mouse é pressionado.
            args (tuple, optional): Argumentos adicionais a serem passados para a função. Default é ().

        """
        self._on_mouse_down = (func, args)

    def set_surface_theme(self, theme: Surface):
        """Define a aparência do controle com base em um tema.

        Args:
            theme (Surface): A superfície contendo a aparência do controle.

        """
        self.__render = theme

    # ========== Call Function's ===========

    def _call_actived(self):
        """Chama a função associada à ativação deste controle, se houver.

        """
        if self._on_actived:
            self._on_actived[0](*self._on_actived[1])

    def _call_on_mouse_down(self):
        """Chama a função definida para ser executada quando o mouse é pressionado sobre o controle.

        Esta função também ativa o controle se ele ainda não estiver ativo.

        """
        self.set_active(True)

        if self._on_mouse_down:
            self._on_mouse_down[0](*self._on_mouse_down[1])

    def _call_on_mouse_up(self):
        """
        Chama a função definida para ser executada quando o mouse é liberado sobre o controle.
        """
        if self._on_mouse_up:
            self._on_mouse_up[0](*self._on_mouse_up[1])

    # ========== Private Function's =========

    def _update_render_rect(self):
        """
        Atualiza o retângulo de renderização do controle.

        Esta função atualiza o retângulo de renderização do controle com base na posição e
        tamanho do retângulo do controle e do retângulo do pai, se houver. Se o controle
        não tiver pai, o retângulo de renderização é definido como o próprio retângulo do controle.
        """
        if self._parent:
            self._render_rect = Rect(self._rect.x + self.parent.rect.x,
                                     self._rect.y + self.parent.rect.y,
                                     self._rect.width, self._rect.height)
        else:
            self._render_rect = self._rect

    # ========== Public Function's ============

    def add_control(self, control):
        """
        Adiciona um controle à janela.

        Args:
            control (Control): O controle a ser adicionado à janela.
        """
        self._controls.append(control)
        control.parent = self

    def move_ip(self, pos_relative):
        """Move o controle relativamente à sua posição atual.

        Args:
            pos_relative (tuple): Uma tupla contendo as coordenadas x e y para mover o controle.

        """
        self.rect.move_ip(pos_relative)
        self._update_render_rect()
        for control in self._controls:
            control._update_render_rect()

    def reset(self):
        """
        Reseta o estado do controle.
        """
        self._is_hovered = False
        self._active = False

        for control in self._controls:
            control.reset()

    def draw(self, screen: Surface):
        """
        Método abstrato para desenhar o controle.
        """
        if self.__render:
            screen.blit(self.__render, self._render_rect)

    def update(self, event: Event):
        """
        Atualiza o estado do controle com base nos eventos fornecidos.

        Args:
            events (Event): Eventos do pygame.
        """
        if not self._visible:
            return
        
        if self._render_rect.collidepoint(mouse.get_pos()):
            if not self._is_hovered:
                self._is_hovered = True
                # TODO Mouse entered function
        else:
            if self._is_hovered:
                self._is_hovered = False
                self._is_clicked = False
                # TODO Mouse leave function

        if self._is_hovered:
            if event.type == constants.MOUSEBUTTONDOWN:
                if not self._is_clicked:
                    self._is_clicked = True
                    self._call_on_mouse_down()
            elif event.type == constants.MOUSEBUTTONUP:
                if self._is_clicked:
                    self._is_clicked = False
                    self._call_on_mouse_up()
        else:
            if event.type == constants.MOUSEBUTTONDOWN:
                self.set_active(False)

        # TODO Implements tab next control
                            