from Nodo import *

'Clase Arista'
class Arista:
    def __init__(self,origen,destino):
        self.origen = origen                        #Guarda el nodo origen
        self.destino = destino                      #Guarda el nodo destino
        self.arista = [Nodo(origen),Nodo(destino)]  #lista para guardar el destino y el origen
        self.atributos = {}                         #Diccionario para sus atributos
