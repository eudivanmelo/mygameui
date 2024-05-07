from pygame import Rect, draw as pydraw, mouse, MOUSEBUTTONDOWN, MOUSEBUTTONUP, image, transform
from pygame.surface import Surface
from pygame.event import Event

class Control:
    """
    Classe base para todos os controles da interface do usuário.

    Attributes:
        _rect (Rect): O retângulo de posição e tamanho do controle.
        _render_rect (Rect): O retângulo de renderização do controle.
        _is_hovered (bool): Indica se o controle está sendo sobrevoado pelo cursor do mouse.
        _is_clicked (bool): Indica se o controle está sendo clicado.
        _visible (bool): Indica se o controle está visível.
        _parent (Control): O controle pai deste controle.
        _on_mouse_up (tuple): A função a ser chamada quando o mouse é liberado sobre o controle.

    Methods:
        parent (getter, setter): Getter e setter para o controle pai deste controle.
        rect (getter): Getter para o retângulo de posição e tamanho do controle.
        x, y (getter, setter): Getters e setters para as coordenadas x e y do controle.
        position (getter): Getter para a posição do controle como uma tupla de coordenadas x e y.
        width, height (getter, setter): Getters e setters para a largura e altura do controle.
        size (getter): Getter para o tamanho do controle como uma tupla de largura e altura.
        visible (getter, setter): Getter e setter para a visibilidade do controle.
        set_on_mouse_up(func, args=()): Define a função a ser chamada quando o mouse é liberado sobre o controle.
        _call_on_mouse_up(): Chama a função definida para ser executada quando o mouse é liberado sobre o controle.
        reset(): Reseta o estado do controle.
        draw(screen: Surface): Método abstrato para desenhar o controle.
        update(events: list[Event]): Atualiza o controle com eventos de entrada.
        __update_render_rect(): Atualiza o retângulo de renderização do controle.
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
        """
        Controle pai deste controle.

        Returns:
            Control: O controle pai deste controle.
        """
        return self._parent
    
    @parent.setter
    def parent(self, control):
        self._parent = control
        self.__update_render_rect()
            
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

    def reset(self):
        """
        Reseta o estado do controle.
        """
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
    """
    Classe para representar uma janela na interface gráfica.

    Args:
        x (int): A coordenada x da posição da janela.
        y (int): A coordenada y da posição da janela.
        width (int): A largura da janela.
        height (int): A altura da janela.
        caption (str, opcional): O texto de legenda da janela (padrão é '').
        closable (bool, opcional): Indica se a janela pode ser fechada (padrão é True).
        movable (bool, opcional): Indica se a janela pode ser movida (padrão é True).

    Attributes:
        __theme (Surface): A superfície que define o tema visual da janela.

    Methods:
        closable (bool): Propriedade para acessar e definir se a janela pode ser fechada.
        set_theme(Surface): Define o tema visual da janela.
        set_theme_bypath(str): Define o tema visual da janela carregando-o de um arquivo de imagem.
        add_control(Control): Adiciona um controle à janela.
        draw(Surface): Desenha a janela na tela.
        update(list[Event]): Atualiza a janela com eventos de entrada.
    """
    def __init__(self, x, y, width, height, caption = '', closable = True, movable = True):
        super().__init__(x, y, width, height)
        self.caption = caption
        self.closable = closable # TODO Implementar essa funcionalidade
        self.movable = movable # TODO Implementar essa funcionalidade

        self._controls: list[Control] = []

        self.__theme: Surface = None

    @property
    def closable(self):
        """
        Propriedade para acessar e definir se a janela pode ser fechada.

        Returns:
            bool: True se a janela pode ser fechada, False caso contrário.
        """
        return self.__closable
    
    @closable.setter
    def closable(self, value: bool):
        self.__closable = value
        if value == True:
            self.__close_button = Button(self._rect.x + self._rect.width - 16, self._rect.y, 16, 16)
            self.__close_button.set_on_mouse_up(lambda: setattr(self, 'visible', False))

    def set_theme(self, theme: Surface):
        """
        Define o tema visual da janela.

        Args:
            theme (Surface): A superfície que define o tema visual da janela.
        """
        self.__theme = theme
        self.__update_render()

    def set_theme_bypath(self, full_path):
        """
        Define o tema visual da janela carregando-o de um arquivo de imagem.

        Args:
            full_path (str): O caminho completo para o arquivo de imagem do tema visual.
        """
        self.__theme = image.load(full_path).convert_alpha()
        self.__update_render()

    def __update_render(self):
        """
        Atualiza as superfícies de renderização da janela com base no tema definido.

        Esta função atualiza as superfícies de renderização que compõem a aparência visual da janela
        com base no tema definido. Ela determina como cada parte da janela deve ser renderizada,
        considerando se a janela é movível ou não, e configura as imagens do botão de fechar
        se a janela for fechável e o botão de fechar estiver presente.

        """
        width = self._rect.width
        heigth = self._rect.height

        ## ===== TOP =======
        if self.movable:
            # Canto superior esquerdo
            self.__render_left_top = self.__theme.subsurface(48, 0, 16, 16)
            # Centro superior
            self.__render_middle_top = transform.scale(self.__theme.subsurface(64, 0, 16, 16), (width - 32, 16))
            # Canto superior direito
            self.__render_right_top = self.__theme.subsurface(80, 0, 16, 16)
        else:
            # Canto superior esquerdo
            self.__render_left_top = self.__theme.subsurface(0, 0, 16, 16)
            # Centro superior
            self.__render_middle_top = transform.scale(self.__theme.subsurface(16, 0, 16, 16), (width - 32, 16))
            # Canto superior direito
            self.__render_right_top = self.__theme.subsurface(32, 0, 16, 16)

        ## ===== MIDDLE =======
        # Canto meio esquerdo
        self.__render_left_middle = transform.scale(self.__theme.subsurface(0, 16, 16, 16), (16, heigth - 32))
        # Centro meio
        self.__render_middle_middle = transform.scale(self.__theme.subsurface(16, 16, 16, 16), (width - 32, heigth - 32))
        # Canto meio direito
        self.__render_right_middle = transform.scale(self.__theme.subsurface(32, 16, 16, 16), (16, heigth - 32))

        ## ===== BOTTOM =======
        # Canto inferior esquerdo
        self.__render_left_bottom = self.__theme.subsurface(0, 32, 16, 16)
        # Centro inferior
        self.__render_middle_bottom = transform.scale(self.__theme.subsurface(16, 32, 16, 16), (width - 32, 16))
        # Canto inferior direito
        self.__render_right_bottom = self.__theme.subsurface(32, 32, 16, 16)

        # Configurar botão de fechar
        if self.closable and self.__close_button:
            self.__close_button.normal_img = self.__theme.subsurface(96, 0, 16, 16)
            self.__close_button.click_img = self.__theme.subsurface(96, 0, 16, 16)
            self.__close_button.hover_img = self.__theme.subsurface(112, 0, 16, 16)

    def add_control(self, control: Control):
        """
        Adiciona um controle à janela.

        Args:
            control (Control): O controle a ser adicionado à janela.
        """
        self._controls.append(control)
        control.parent = self

    def draw(self, screen):
        if not self.visible:
            return # Não mostrar controle caso ele não esteja visível
        
        x = self._rect.x
        y = self._rect.y
        
        if self.__theme:
            ## ===== TOP =======
            screen.blit(self.__render_left_top, (x, y))
            screen.blit(self.__render_middle_top, (x + 16, y))
            screen.blit(self.__render_right_top, (x + (self._rect.width - 16), y))
            ## ===== MIDDLE =======
            screen.blit(self.__render_left_middle, (x, y + 16))
            screen.blit(self.__render_middle_middle, (x + 16, y + 16))
            screen.blit(self.__render_right_middle, (x + (self._rect.width - 16), y + 16))
            ## ===== MIDDLE =======
            screen.blit(self.__render_left_bottom, (x, y + (self._rect.height - 16)))
            screen.blit(self.__render_middle_bottom, (x + 16, y + (self._rect.height - 16)))
            screen.blit(self.__render_right_bottom, (x + (self._rect.width - 16), y + (self._rect.height - 16)))

        if self.closable and self.__close_button:
            self.__close_button.draw(screen)

        # Render controls in order
        for control in self._controls:
            control.draw(screen)

    def update(self, events: list[Event]):
        if not self.visible:
            return # Não atualizar controle caso ele não esteja visível
        
        if self.closable and self.__close_button:
            self.__close_button.update(events)

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