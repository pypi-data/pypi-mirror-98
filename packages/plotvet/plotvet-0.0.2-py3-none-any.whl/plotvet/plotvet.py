import numpy as np
import matplotlib.pyplot as plt

def plota2D(lista_vetores, lista_cores, lista_limites):
    plt.figure()
    plt.axvline(x=0, color='#A9A9A9', zorder=0)
    plt.axhline(y=0, color='#A9A9A9', zorder=0)

    for i in range(len(lista_vetores)):
        x = np.concatenate([[0,0],lista_vetores[i]])
        plt.quiver([x[0]],
                   [x[1]],
                   [x[2]],
                   [x[3]],
                   angles='xy', scale_units='xy', scale=1, color=lista_cores[i],
                  alpha=1)
    plt.xlim(lista_limites[0], lista_limites[1])
    plt.ylim(lista_limites[2], lista_limites[3])
    plt.show()


def plota3D(lista_vetores, lista_cores, lista_limites):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlim3d(lista_limites[0], lista_limites[1])
    ax.set_ylim3d(lista_limites[2], lista_limites[3])
    ax.set_zlim3d(lista_limites[4], lista_limites[5])
    i = 0
    for vector in lista_vetores:
        ax.quiver(0, 0, 0, vector[0], vector[1], vector[2], length=1, normalize=False, color=lista_cores[i])
        i += 1
    plt.show()
