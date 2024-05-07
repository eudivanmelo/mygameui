from pygame import Surface
from pygame.transform import scale

def generate_surface_byrect(surface: Surface, width, height):
    """
    Gera uma nova Surface dividindo a Surface fornecida em nove regiões
    e as compondo em uma nova Surface com a largura e altura especificadas.

    Args:
        surface (Surface): A Surface original a ser dividida.
        width (int): A largura da nova Surface.
        height (int): A altura da nova Surface.

    Returns:
        Surface: Uma nova Surface composta por nove regiões da Surface original.

    Observação:
        Espera-se que a Surface de entrada tenha um tamanho que seja múltiplo de três em ambas as dimensões.
        As regiões são divididas da seguinte forma:
        - A Surface original é dividida em nove retângulos de tamanho igual.
        - O retângulo central permanece sem escala e é posicionado no centro da nova Surface.
        - Os retângulos de canto mantêm seu tamanho original e são posicionados nos cantos da nova Surface.
        - Os retângulos restantes são escalonados para se ajustarem ao espaço disponível e são posicionados conforme necessário.
    """
    new_surface = Surface((width, height)).convert_alpha()
    new_surface.fill((0,0,0,0))

    # Calculate tile size
    t_width = surface.get_rect().width // 3
    t_height = surface.get_rect().height // 3
    rest_horizontal = (surface.get_width() - (t_width * 2))
    rest_vertical = (surface.get_height() - (t_height * 2))

    ## ===== TOP =====
    # Top Left
    sub_s = surface.subsurface(0, 0, t_width, t_height)
    pos = (0, 0)
    new_surface.blit(sub_s, pos)

    # Top Middle
    sub_s = surface.subsurface(t_width, 0, rest_horizontal, t_height)
    pos = (t_width, 0)
    t_scale = (width - (t_width * 2), t_height)
    new_surface.blit(scale(sub_s, t_scale), pos)
    
    # Top Right
    sub_s = surface.subsurface(t_width + rest_horizontal, 0, t_width, t_height)
    pos = (width - t_width, 0)
    new_surface.blit(sub_s, pos) 


    ## ===== MIDDLE =====
    # Middle Left
    sub_s = surface.subsurface(0, t_height, t_width, t_height)
    pos = (0, t_height)
    t_scale = (t_width, height - (t_height * 2))
    new_surface.blit(scale(sub_s, t_scale), pos)

    # Middle Middle
    sub_s = surface.subsurface(t_width, t_height, rest_horizontal, rest_vertical)
    pos = (t_width, t_height)
    t_scale = (width - (t_width * 2), height - (t_height * 2))
    new_surface.blit(scale(sub_s, t_scale), pos)
    
    # Middle Right
    sub_s = surface.subsurface(t_width + rest_horizontal, t_height, t_width, t_height)
    pos = (width - t_width, t_height)
    t_scale = (t_width, height - (t_height * 2))
    new_surface.blit(scale(sub_s, t_scale), pos)

    ## ===== BOTTON =====
    # Botton Left
    sub_s = surface.subsurface(0 , t_height + rest_vertical, t_width, t_height)
    pos = (0, height - t_height)
    new_surface.blit(sub_s, pos)

    # Botton Middle
    sub_s = surface.subsurface(t_width, t_height + rest_vertical, rest_horizontal, t_height)
    pos = (t_width, height - t_height)
    t_scale = (width - (t_width * 2), t_height)
    new_surface.blit(scale(sub_s, t_scale), pos)
    
    # Botton Right
    sub_s = surface.subsurface(t_width + rest_horizontal, t_height + rest_vertical, t_width, t_height)
    pos = (width - t_width, height - t_height)
    new_surface.blit(sub_s, pos) 

    return new_surface