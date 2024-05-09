# MyGameUI

MyGameUI é uma biblioteca Python desenvolvida para criar interfaces de usuário (UI) simples em jogos 2D usando Pygame. Esta biblioteca oferece uma variedade de controles básicos, como janelas e botões, para facilitar a criação de interfaces de usuário interativas e responsivas em seus projetos.

## Classes

### `Control`

- **Descrição**: Classe base para todos os controles da interface do usuário.
- **Funcionalidades**:
    - Gerenciamento de posição e tamanho do controle.
    - Capacidade de definir se o controle está visível ou não.
    - Suporte para eventos de mouse, como clicar e mover o mouse sobre o controle.
    - Possibilidade de adicionar controles filhos e definir um controle pai.
    - Personalização da aparência do controle com base em um tema.

### `Form`

- **Descrição**: Representa uma janela de formulário na interface do usuário.
- **Funcionalidades**:
    - Define a aparência do formulário com base em um tema.
    - Define a imagem do formulário manualmente.
    - Desenha o formulário na tela especificada.
    - Atualiza o formulário com base nos eventos recebidos.

### `Button`

- **Descrição**: Representa um botão clicável em uma interface de usuário.
- **Funcionalidades**:
    - Define a aparência do botão com base em um tema Surface.
    - Desenha o botão na tela especificada.

### `Textbox`

- **Descrição**: Representa um controle de caixa de texto que pode ser usado para entrada de texto.
- **Funcionalidades**:
    - Define o tema visual do textbox.
    - Define uma função a ser chamada sempre que o texto dentro do textbox for alterado.
    - Desenha o textbox na tela especificada.
    - Atualiza o textbox com base nos eventos recebidos.

## Instalação

Para instalar a biblioteca MyGameUI, você pode clonar este repositório Git ou instalá-lo usando o pip.

```bash
pip install git+https://github.com/eudivanmelo/mygameui.git
```

## Exemplo de Uso

Aqui está um exemplo simples de como usar as classes Window e Button em um projeto de jogo:

```python
import pygame
from mygameui import Form, Button

# Inicialize o Pygame
pygame.init()

# Defina as dimensões da janela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Exemplo de UI")

# Crie uma janela principal
test_window = Form(100, 100, 600, 400)

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

