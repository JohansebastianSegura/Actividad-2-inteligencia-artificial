import random, sys, math

# Genera una tabla de distancias entre puntos.
def generarMatrizDistancias(numNodos, maxDistancia):
    matrizDist = [[0 for i in range(numNodos)] for j in range(numNodos)]
    
    for i in range(numNodos):
        for j in range(i):
            matrizDist[i][j] = maxDistancia * random.random()
            matrizDist[j][i] = matrizDist[i][j]
        
    return matrizDist

# Selecciona el siguiente nodo a visitar basado en las distancias y las marcas dejadas.
def seleccionarNodo(distancias, marcas, nodosVisitados):
    pesosNodos = []
    opcionesDisponibles = []
    nodoActual = nodosVisitados[-1]
    
    alfa = 1.0  # Influencia de las marcas
    beta = 0.5  # Influencia de las distancias
    
    for i in range(len(distancias)):
        if i not in nodosVisitados:
            influenciaMarcas = math.pow((1.0 + marcas[nodoActual][i]), alfa)
            peso = math.pow(1.0 / distancias[nodoActual][i], beta) * influenciaMarcas
            opcionesDisponibles.append(i)
            pesosNodos.append(peso)
    
    # Selección aleatoria ponderada basada en los pesos calculados.
    seleccionAleatoria = random.random() * sum(pesosNodos)
    sumaPesos = 0.0
    indiceSeleccionado = -1
    
    while seleccionAleatoria > sumaPesos:
        indiceSeleccionado += 1
        sumaPesos += pesosNodos[indiceSeleccionado]
        
    return opcionesDisponibles[indiceSeleccionado]

# Encuentra un recorrido completo por todos los nodos basado en distancias y marcas.
def buscarRecorrido(distancias, marcas):
    recorrido = [0]  # Inicia en el nodo 0
    longitudRecorrido = 0
    
    while len(recorrido) < len(distancias):
        nodoSiguiente = seleccionarNodo(distancias, marcas, recorrido)
        longitudRecorrido += distancias[recorrido[-1]][nodoSiguiente]
        recorrido.append(nodoSiguiente)
    
    # Regreso al nodo inicial para completar el ciclo.
    longitudRecorrido += distancias[recorrido[-1]][0]
    recorrido.append(0)
    
    return (recorrido, longitudRecorrido)

# Actualiza las marcas dejadas en el camino recorrido.
def actualizarMarcas(marcas, recorrido, incremento):
    for i in range(len(recorrido) - 1):
        marcas[recorrido[i]][recorrido[i+1]] += incremento

# Reduce las marcas en todas las rutas, simulando la evaporación.
def evaporarMarcas(marcas):
    for fila in marcas:
        for i in range(len(fila)):
            fila[i] *= 0.9

# Algoritmo principal para encontrar el mejor recorrido.
def algoritmoHormigas(distancias, numIteraciones, promedioDist):
    numNodos = len(distancias)
    marcas = [[0 for i in range(numNodos)] for j in range(numNodos)]
    
    mejorRecorrido = []
    mejorLongitud = sys.maxsize
    
    for iteracion in range(numIteraciones):
        (recorrido, longitud) = buscarRecorrido(distancias, marcas)
        
        if longitud <= mejorLongitud:
            mejorRecorrido = recorrido
            mejorLongitud = longitud
        
        actualizarMarcas(marcas, recorrido, promedioDist / longitud)
        evaporarMarcas(marcas)
    
    return (mejorRecorrido, mejorLongitud)

# Prueba del algoritmo con una matriz de distancias generada aleatoriamente.
nodos = 4
distanciaMax = 4
tablaDistancias = generarMatrizDistancias(nodos, distanciaMax)

numIteraciones = 1000
distanciaPromedio = nodos * distanciaMax / 2
(mejorRecorrido, mejorLongitud) = algoritmoHormigas(tablaDistancias, numIteraciones, distanciaPromedio)
print("Resultados obtenidos por el algoritmo para la actividad 2")
print("############ Mejor recorrido: ", mejorRecorrido, "###################")
print("############ Longitud del mejor recorrido: ", mejorLongitud, "###########")
