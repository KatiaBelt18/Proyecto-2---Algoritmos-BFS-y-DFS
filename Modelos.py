from Nodo import *
from Grafo import *
from Arista import * 
import random
import math

'''
Grafo de Erdös y Rényi
Genera un grafo aleatorio según el modelo de Erdős y Rényi G(n, m)
donde n es el número de nodos y m es el número de aristas.
Si 'dirigido' es True, se podría adaptar para grafos dirigidos.
'''

def grafo_ErdosRenyi(n, m, dirigido=False):
    grafo = Grafo()                             # Se crea una instancia vacía del grafo.

    # Se agregan n nodos numerados del 0 al n-1 al grafo.
    for i in range(n):
        grafo.agregar_Nodo(i)

    # Se generan todos los pares posibles de nodos (i, j) con i < j.
    # Esto corresponde a todas las posibles aristas no dirigidas sin repetición.
    aristas = []
    for i in range(n):
        for j in range(i + 1, n):
            aristas.append((i, j))

    # Se seleccionan aleatoriamente m aristas únicas del conjunto de posibles aristas.
    aristas_seleccionadas = random.sample(aristas, m)

    # Se agregan las aristas seleccionadas al grafo.
    for (i, j) in aristas_seleccionadas:
        grafo.agregar_Arista(grafo.nodos[i], grafo.nodos[j])

    return grafo                                # Se devuelve el grafo generado.


'''
Grafo de Gilbert
Genera un grafo aleatorio siguiendo el modelo de Gilbert G(n, p),
donde n es el número de nodos y p es la probabilidad (0-100) de que exista una arista entre cada par de nodos.
Si 'dirigido' es True, se puede adaptar a grafos dirigidos.
'''

def grafo_Gilbert(n, p, dirigido=False):
    grafo = Grafo()                             # Crea una instancia vacía del grafo
    nodos = []                                  # Lista de nodos para facilitar iteraciones
    aristas = []                                # Lista para registrar aristas ya agregadas y evitar duplicados

    # Se crean n nodos numerados del 0 al n-1
    for i in range(n):
        grafo.agregar_Nodo(i)
        nodos.append(i)

    # Se intenta conectar cada par de nodos distintos con una probabilidad p
    for i in nodos:
        for j in nodos:
            if i == j:
                continue  # Se evita agregar lazos (aristas de un nodo a sí mismo)

            prob = random.random()                           # Número aleatorio entre 0 y 1
            # Si la probabilidad es menor o igual a p (ajustada a escala 0-1), y la arista aún no existe
            if prob <= (p / 100) and [i, j] not in aristas and [j, i] not in aristas:
                grafo.agregar_Arista(i, j)                   # Se agrega la arista
                aristas.append([i, j])                       # Se guarda para evitar duplicados (para grafos no dirigidos)

    return grafo                                             # Devuelve el grafo generado


'''
Grafo graográfico simple
Genera un grafo geográfico aleatorio:
Crea n nodos ubicados aleatoriamente en el plano 2D dentro del cuadrado (0,0)-(1,1).
Conecta dos nodos si la distancia euclidiana entre ellos es menor o igual a un radio r.
'''

def grafo_Geografico(n, r, dirigido=False):
    grafo = Grafo()                                         # Se crea una instancia vacía del grafo
    nodos = list(range(1, n + 1))                           # Lista de identificadores de nodos (desde 1 hasta n)
    pos = []                                                # Guarda las coordenadas aleatorias (x, y) de cada nodo
    aristas = []                                            # Guarda las aristas agregadas (no necesario si no se usan luego)

    # Crear nodos con coordenadas aleatorias entre 0 y 1
    for i in nodos:
        grafo.agregar_Nodo(i)                               # Agrega el nodo al grafo
        x = random.random()                                 # Coordenada x aleatoria
        y = random.random()                                 # Coordenada y aleatoria
        pos.append((x, y))                                  # Guarda la posición del nodo

    # Conectar nodos cuya distancia sea menor o igual a r
    for i in range(n):
        for j in range(i + 1, n):                           # Solo considera pares i < j para evitar duplicados y lazos
            x1, y1 = pos[i]
            x2, y2 = pos[j]
            distancia = math.hypot(x2 - x1, y2 - y1)        # Calcula distancia euclidiana
            if distancia <= r:
                grafo.agregar_Arista(nodos[i], nodos[j])    # Agrega arista entre los nodos
                aristas.append((nodos[i], nodos[j]))        # Guarda la arista (opcional)

    return grafo  # Devuelve el grafo construido


'''
Grafo Barabasi Albert
Genera un grafo inspirado en el modelo de Barabási-Albert.
Crea un grafo con n nodos donde cada nodo se conecta con probabilidad dependiente del grado.
El parámetro d limita el número máximo de conexiones por nodo.
'''

def grafo_BarabasiAlbert(n, d, dirigido=False):
    grafo = Grafo()                                         # Se crea una instancia vacía del grafo
    aristas = []                                            # Lista para guardar las aristas agregadas (opcional)
    grados = [0] * n                                        # Lista que almacena el grado de cada nodo (inicialmente 0)

    # Se agregan n nodos numerados del 1 al n
    for i in range(n):
        grafo.agregar_Nodo(i + 1)

    # Se intenta conectar cada par de nodos (i, j), con j > i
    for i in range(n):
        for j in range(i + 1, n):
            # Solo se conecta si ambos nodos aún no alcanzan el grado máximo d
            if grados[i] < d and grados[j] < d:
                # Se calcula la probabilidad de conexión según el grado actual
                p_i = 1 - (grados[i] / d)
                p_j = 1 - (grados[j] / d)
                p = min(p_i, p_j)                           # Probabilidad de conexión conjunta

                # Si la probabilidad es suficientemente alta, se agrega la arista
                if random.random() < p:
                    grafo.agregar_Arista(i + 1, j + 1)
                    aristas.append((i + 1, j + 1))
                    grados[i] += 1
                    grados[j] += 1

    return grafo                                            # Devuelve el grafo construido


'''
Grafo Dorogovtsev-Mendes'
Genera un grafo según el modelo Doro-Mendes.
El grafo comienza con un triángulo y crece agregando nodos que se conectan a aristas existentes.
'''

def grafo_DoroMendes(n, dirigido = False):
    grafo = Grafo()                         # Se crea una instancia vacía del grafo
    nodos = list(range(1, n + 1))           # Lista de nodos numerados desde 1 hasta n
    aristas = []                            # Lista que almacenará las aristas actuales


    #Crear 3 nodos y conectarlos formando un triángulo
    for i in range(3):
        grafo.agregar_Nodo(nodos[i])        # Se agregan los nodos 1, 2 y 3
    

    #Conectar los 3 nodos entre sí para formar el triángulo inicial
    grafo.agregar_Arista(nodos[0], nodos[1])
    aristas.append([nodos[0], nodos[1]])

    grafo.agregar_Arista(nodos[1], nodos[2])
    aristas.append([nodos[1], nodos[2]])

    grafo.agregar_Arista(nodos[2], nodos[0])
    aristas.append([nodos[2], nodos[0]])

    #Agregar nodos restantes (desde el 4to en adelante)
    for i in range(3, n):
        nuevo = nodos[i]                    # Selecciona el nuevo nodo a insertar
        grafo.agregar_Nodo(nuevo)           # Lo agrega al grafo
    
        # Seleccionar una arista existente al azar
        a, b = random.choice(aristas)

        # Conectar el nuevo nodo a ambos extremos de la arista
        grafo.agregar_Arista(nuevo, a)
        grafo.agregar_Arista(nuevo, b)

        # Registrar nuevas aristas
        aristas.append((nuevo, a))
        aristas.append((nuevo, b))           # Se retorna el grafo generado

    return grafo

'''
Grafo de malla'
Genera un grafo en forma de malla (grid) de tamaño m x n.
Cada nodo se conecta a su vecino derecho y su vecino inferior, si existen.
'''

def grafo_Malla(m, n):
    grafo = Grafo()                 # Se crea una instancia vacía del grafo
    aristas = []                    # Lista para almacenar las aristas creadas

    # Crear nodos numerados del 1 al m*n y asignarlos a coordenadas (i, j)
    nodos = {}                      # Diccionario para mapear coordenadas (i,j) al id del nodo
    id = 1                          # Identificador único para cada nodo

    for i in range(m):              # Recorre las filas
        for j in range(n):          # Recorre las columnas
            nodos[(i, j)] = id      # Asigna un ID al nodo en la posición (i, j)
            grafo.agregar_Nodo(id)  # Agrega el nodo al grafo
            id += 1
    # Crear aristas entre cada nodo y sus vecinos derecho y abajo
    for i in range(m):
        for j in range(n):
            actual = nodos[(i, j)]  # Nodo actual en (i, j)
            if j + 1 < n:           # Si existe un vecino a la derecha
                derecha = nodos[(i, j + 1)]
                grafo.agregar_Arista(actual, derecha)  # Conectar con el nodo derecho
                aristas.append((actual, derecha))
            if j + 1 < n:           # Si existe un vecino a la derecha
                derecha = nodos[(i, j + 1)]
                grafo.agregar_Arista(actual, derecha)  # Conectar con el nodo derecho
                aristas.append((actual, derecha))
    return grafo                    # Devuelve el grafo con estructura de malla
