import random

# Función objetivo
def funcion(x, y, z):
    """Función objetivo a maximizar."""
    return x ** 2 + (y / z)

# Decodificar binario a entero
def binario_a_entero(binario, bounds):
    min_bound, max_bound = bounds
    decimal = int(binario, 2)
    return min_bound + (decimal / (2**len(binario) - 1)) * (max_bound - min_bound)

# Generar un individuo aleatorio en binario
def generar_individuo(bounds, bits=5):
    return ''.join([random.choice(['0', '1']) for _ in range(bits)])

# Evaluar la función objetivo para un individuo
def evaluar_individuo(individuo, bounds):
    x_bin, y_bin, z_bin = individuo
    x = binario_a_entero(x_bin, bounds)
    y = binario_a_entero(y_bin, bounds)
    z = binario_a_entero(z_bin, bounds)
    if z == 0:  # Evitar la división entre 0
        z = 1
    return funcion(x, y, z)

# Selección por torneo
def seleccion_torneo(poblacion, fitness, k=2):
    participantes = random.sample(list(enumerate(fitness)), k)
    ganador = max(participantes, key=lambda x: x[1])
    return poblacion[ganador[0]]

# Cruzamiento de un punto
def cruzamiento_binario(padre1, padre2):
    punto_cruce = random.randint(1, len(padre1[0]) - 1)
    hijo1 = [padre1[i][:punto_cruce] + padre2[i][punto_cruce:] for i in range(3)]
    hijo2 = [padre2[i][:punto_cruce] + padre1[i][punto_cruce:] for i in range(3)]
    return hijo1, hijo2

# Mutación
def mutacion(individuo, tasa_mutacion=0.1):
    mutado = []
    for gen in individuo:
        nuevo_gen = ''.join(
            [str(1 - int(bit)) if random.random() < tasa_mutacion else bit for bit in gen]
        )
        mutado.append(nuevo_gen)
    return mutado

# Generar población y cruzar
def generar_poblacion_y_cruzar():
    # Parámetros
    bounds = [-10, 10]
    pop_size = 2
    bits = 5

    # Generar población inicial
    poblacion = [[generar_individuo(bounds, bits) for _ in range(3)] for _ in range(pop_size)]
    
    # Evaluar padres
    fitness = [evaluar_individuo(ind, bounds) for ind in poblacion]
    
    # Seleccionar padres
    padre1 = poblacion[0]
    padre2 = poblacion[1]
    
    # Cruzamiento
    hijos = []
    for _ in range(2):
        hijo1, hijo2 = cruzamiento_binario(padre1, padre2)
        hijo1 = mutacion(hijo1)
        hijo2 = mutacion(hijo2)
        hijos.extend([hijo1, hijo2])
    
    # Evaluar fitness de los padres
    fitness_padre1 = fitness[0]
    fitness_padre2 = fitness[1]
    
    # Imprimir resultados
    print(f"Padre 1: {padre1} -> x = {padre1[0]}, y = {padre1[1]}, z = {padre1[2]}")
    print(f"Padre 2: {padre2} -> x = {padre2[0]}, y = {padre2[1]}, z = {padre2[2]}\n")

    for i, hijo in enumerate(hijos, start=1):
        print(f"Hijo {i}: {hijo}")

    print(f"\nFunción objetivo Padre 1: {fitness_padre1}")
    print(f"Función objetivo Padre 2: {fitness_padre2}\n")

# Ejecutar el programa
if __name__ == "__main__":
    generar_poblacion_y_cruzar()
