from pygame import image, font as pgfont, init
from os.path import join
from pkg_resources import resource_filename

init()
theme = image.load(resource_filename('mygameui', join('imgs', 'default.png')))

font = pgfont.SysFont('consolas', 12)