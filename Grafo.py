from Nodo import *
from Arista import *

'Clase Grafo'
class Grafo: 
    def __init__(self):
        self.nodos = []         # Lista para almacenar los nodos del grafo
        self.aristas = []       # Lista para almacenar las aristas como pares de nodos
        self.atributos = {}     # Diccionario para atributos adicionales (opcional, no se usa aquí)

    def agregar_Nodo(self, n):
        # Agrega un nodo al grafo si no está ya presente
        if n not in self.nodos:
            nodo = Nodo(n)                          # Crea una instancia de Nodo (se espera que exista esta clase)
            self.nodos.append(nodo.identificador)   # Agrega el identificador del nodo a la lista de nodos

    def agregar_Arista(self, origen, destino):
        #Agrega una arista entre dos nodos si ambos están en el grafo
        if origen in self.nodos and destino in self.nodos:
            aristas_id = Arista(origen, destino)    # Crea una instancia de Arista (se espera que exista esta clase)
            self.aristas.append([
                aristas_id.arista[0].identificador, 
                aristas_id.arista[1].identificador
            ])  # Agrega la arista como una lista de dos nodos

    def mostrar_grafo(self):
        # Imprime los nodos del grafo
        print("Nodos:")
        for nodo in self.nodos:
            print(f"  Nodo {nodo}")

        # Imprime las aristas del grafo
        print("\nAristas:")
        for arista in self.aristas:
            print(f"  {arista[0]} -> {arista[1]}")

    def exportar_a_gv(self, nombre_archivo):
        # Exporta el grafo a un archivo en formato Graphviz (.gv)
        with open(nombre_archivo, 'w') as f:
            f.write('graph G {\n')                   # Inicio de un grafo no dirigido
            
            usadas = set()                           # Conjunto para evitar duplicar aristas
            for arista in self.aristas:
                n1, n2 = arista
                if (n2, n1) not in usadas:           # Evita escribir aristas duplicadas
                    f.write(f'    {n1} -- {n2};\n')  # Sintaxis de grafo no dirigido
                    usadas.add((n1, n2))

            # Agrega nodos que no tienen ninguna arista
            for i in range(len(self.nodos)):
                b = False
                while not b:
                    for j in range(len(self.aristas)):
                        if self.nodos[i] in self.aristas[j]:
                            b = True                 # El nodo tiene al menos una arista
                    if not b:
                        ns = str(self.nodos[i])
                        f.write(f'    {ns};\n')      # Nodo aislado
                    b = True                         # Salir del while (se ejecuta solo una vez)

            f.write('}\n')                           # Cierra el bloque del grafo

    def exportar_a_gv_algoritmo(self, nombre_archivo):
        if not hasattr(self, 'bfs_resultado'):
            print("Primero debes ejecutar BFS para tener los datos del recorrido.")
            return

        capas = self.bfs_resultado['capas']
        padres = self.bfs_resultado['padres']
        visitados = self.bfs_resultado['visitados']

        with open(nombre_archivo, 'w') as f:
            f.write('digraph G {\n')  # Grafo dirigido

            # Escribir nodos
            for nodo in visitados:
                f.write(f'    {nodo};\n')

            # Escribir aristas padre -> hijo
            for hijo, padre in padres.items():
                f.write(f'    {padre} -> {hijo};\n')

            f.write('}\n')

        print(f"Grafo exportado correctamente a {nombre_archivo}")

    def exportar_arbol_dfs_a_gv(self,arbol_dfs, nombre_archivo):
        """
        Exporta el árbol DFS (como lista de aristas) a un archivo .gv para usar en Gephi.
        """
        with open(nombre_archivo, 'w') as f:
            f.write('digraph G {\n')  # DFS es dirigido (usamos digraph)

            nodos_usados = set()

            for origen, destino in arbol_dfs:
                f.write(f'    {origen} -> {destino};\n')
                nodos_usados.add(origen)
                nodos_usados.add(destino)

            # Si algún nodo no aparece en ninguna arista, lo agregamos como nodo aislado
            for nodo in self.nodos:
                if nodo not in nodos_usados:
                    f.write(f'    {nodo};\n')

            f.write('}\n')



    """
    METODOS DE LA CLASE GRAFO PARA LOS ALGORITMOS BFS Y DFS
    """
    #Búsqueda a lo ancho 
    'Genera un árbol a partir de un grao. Explora desde s y hacia fuera'
    'en todas direcciones posibles, añadiendo nodos una capa a la vez.'
    'param: self -> grafo'
    'param: s    -> nodo'

    def BFS(self, s):
        print("Algoritmo BFS\n")
        
        layer = []                # Lista de capas (cada capa es una lista de nodos)
        cont_capa = 0             # Contador de capa
        nodo_descubierto = []     # Lista para nodos descubiertos
        padres = {}               # Diccionario de descubridores
        nodeSource = None         # Nodo fuente

        if s not in self.nodos:
            print("No se encuentra el nodo en el modelo")
            return False

        nodeSource = s
        nodo_descubierto.append(nodeSource)
        layer.append([nodeSource])  # Capa 0

        while layer[cont_capa]:
            nueva_capa = []

            for u in layer[cont_capa]:
                vecinos = []
                for arista in self.aristas:
                    a, b = arista
                    if a == u and b not in nodo_descubierto:
                        vecinos.append(b)
                    elif b == u and a not in nodo_descubierto:
                        vecinos.append(a)

                for v in vecinos:
                    if v not in nodo_descubierto:
                        nodo_descubierto.append(v)
                        nueva_capa.append(v)
                        padres[v] = u  # u descubrió a v

            layer.append(nueva_capa)
            cont_capa += 1

        if not layer[-1]:
            layer.pop()

        for i, capa in enumerate(layer):
            print(f"Capa {i}: {capa}")

        # Guardar resultado del recorrido
        self.bfs_resultado = {
            'capas': layer,
            'padres': padres,
            'visitados': nodo_descubierto
        }

        return self.bfs_resultado

                

    #Busqueda en profundidad
    def DFS_recursiva(self, s, explorados=None, arbol=None):
        """
        DFS recursiva desde un nodo s.
        - s: nodo origen
        - explorados: conjunto de nodos visitados
        - arbol: lista de aristas (tuplas) que forman el árbol DFS
        """
        if s not in self.nodos:
            print("El nodo no pertenece al modelo")
            return False

        if explorados is None:
            explorados = set()
        if arbol is None:
            arbol = []

        explorados.add(s)

        # Obtener vecinos del nodo actual
        vecinos = []
        for a, b in self.aristas:
            if a == s and b not in explorados:
                vecinos.append(b)
            elif b == s and a not in explorados:
                vecinos.append(a)

        # Recorrer vecinos no explorados
        for v in vecinos:
            if v not in explorados:
                arbol.append((s, v))  # Agregar arista al árbol DFS
                self.DFS_recursiva(v, explorados, arbol)

        return arbol

        
    def DFS_iterativa(self, s):
        if s not in self.nodos:
            print("El nodo no pertenece al modelo")
            return False

        visitados = set()
        arbol_dfs = []
        stack = [(s, None)]  # Pila de tuplas (nodo, padre), el padre de s es None

        while stack:
            u, padre = stack.pop()

            if u not in visitados:
                visitados.add(u)

                if padre is not None:
                    arbol_dfs.append((padre, u))  # Registrar la arista desde el padre a u

                # Buscar vecinos no visitados
                vecinos = []
                for a, b in self.aristas:
                    if a == u and b not in visitados:
                        vecinos.append(b)
                    elif b == u and a not in visitados:
                        vecinos.append(a)

                # Agregar vecinos con el nodo actual como padre
                for v in reversed(vecinos):  # reversed para DFS correcto
                    stack.append((v, u))

        return arbol_dfs


        
    

    



        
