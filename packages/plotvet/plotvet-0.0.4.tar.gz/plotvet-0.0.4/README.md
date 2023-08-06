# plotvet

**plotvet** é um pacote simples e fácil para plotar vetores no espaço bidimensional e tridimensional.

## Dependências
**Python 3.6** ou posterior

Pacote **numpy**
Pacote **matplotlib.pyplot**


## Começando o uso
Você vai precisar instalar o pacote **plotvet**, para isso basta executar:
```
pip install plotvet
```

## Funções

* `plota2D([<lista de vetores>],[<lista de cores para cada vetor],[<limites da plotage 2D>])` - Plota vetores no espaço bidimensional
```
Ex: 
u_laranja='#FF9A13'
v_azul='#1190FF'
r_vermelho='#FF0000'

u=[1,2]
v=[2,1]
u=np.array(u)
v=np.array(v)
r=u+v

plota2D([u,v,r],[u_laranja,v_azul,r_vermelho],[-3,3,-3,3])
```
* `plota3D([<lista de vetores>],[<lista de cores para cada vetor],[<limites da plotage 3D>])` - Plota vetores no espaço tridimensional
```
Ex: 
u_laranja='#FF9A13'
v_azul='#1190FF'
r_vermelho='#FF0000'

u=[-1,1,2]
v=[2,3,2]
u=np.array(u)
v=np.array(v)
r=u+v

plota3D([u,v,r],[u_laranja,v_azul,r_vermelho],[-4,4,-4,4,-4,4])
```