from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='plotvet',
    version='0.0.8',
    url='https://github.com/marcos-de-sousa/plotvet',
    license='MIT License',
    author='Marcos Paulo Alves de Sousa',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='desousa.mpa@gmail.com',
    keywords='Pacote',
    description='Pacote python para plotagem de vetores em planos bidimensionais e espaços tridimensionais',
    packages=['plotvet'],
    install_requires=['numpy','matplotlib'])