# MyGameUI

MyGameUI é uma biblioteca Python desenvolvida para criar interfaces de usuário (UI) simples em jogos 2D usando Pygame. Esta biblioteca oferece uma variedade de controles básicos, como janelas e botões, para facilitar a criação de interfaces de usuário interativas e responsivas em seus projetos.

## Classes

### `Control`

- **Descrição**: Classe base para todos os controles da interface do usuário.
- **Funcionalidades**:
    - Controla a posição, tamanho, visibilidade e interações dos controles.

### `Window`

- **Descrição**: Representa uma janela que pode conter outros controles.
- **Funcionalidades**:
    - Adiciona e gerencia controles filhos.

### `Button`

- **Descrição**: Classe para criar um botão clicável.
- **Funcionalidades**:
    - Permite definir texto e imagens para diferentes estados do botão (normal, hover e clicado).
    - Gerencia interações de clique do mouse.

## Instalação

Para instalar a biblioteca MyGameUI, você pode clonar este repositório Git ou instalá-lo usando o pip.

```bash
pip install git+https://github.com/eudivanmelo/mygameui.git
```

## Exemplo de Uso

Aqui está um exemplo simples de como usar as classes Window e Button em um projeto de jogo:

```python
import pygame
from mygameui import Window, Button

# Inicialize o Pygame
pygame.init()

# Defina as dimensões da janela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Exemplo de UI")

# Crie uma janela principal
test_window = Window(100, 100, 600, 400)

# Crie um botão e adicione à janela principal
b = Button(50, 50, 100, 50, text="Clique Aqui")
test_window.add_control(b)

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Atualize a janela principal
    test_window.update(pygame.event.get())

    # Limpe a tela
    screen.fill((255, 255, 255))

    # Desenhe a janela principal e seus controles
    test_window.draw(screen)

    # Atualize a tela
    pygame.display.flip()
```

Isso criará uma janela com um botão clicável. Você pode expandir essa estrutura adicionando mais controles e funcionalidades conforme necessário.

## Licença

Este projeto é licenciado sob a [Licença MIT](LICENSE). Consulte o arquivo [LICENSE](LICENSE) para obter mais informações.

