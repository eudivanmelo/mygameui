from setuptools import setup, find_packages

setup(
    name='mygameui',
    version='0.1',
    description='Uma biblioteca para criação de interfaces de usuário em pygame',
    author='Eudivan de Melo e Silva Junior',
    author_email='eudivan.mjunior@gmail.com',
    packages=find_packages(),
    package_data={'mygameui': ['imgs/*.png']},
    install_requires=['pygame'],
)