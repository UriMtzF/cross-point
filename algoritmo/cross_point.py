import random
import json

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

# Evaluar la función objetivo para una población
def evaluar_poblacion(poblacion, bounds):
    fitness = []
    for ind in poblacion:
        x_bin, y_bin, z_bin = ind
        x = binario_a_entero(x_bin, bounds)
        y = binario_a_entero(y_bin, bounds)
        z = binario_a_entero(z_bin, bounds)
        if z == 0:  # Evitar la división entre 0
            z = 1
        fitness.append(funcion(x, y, z))
    return fitness

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

# algoritmo genético
def algoritmo_genetico(bounds, pop_size=4, generaciones=10, bits=5):
    # Inicializar población
    poblacion = [[generar_individuo(bounds, bits) for _ in range(3)] for _ in range(pop_size)]
    
    for gen in range(generaciones):
        print(f"\nGeneración {gen+1}")
        print("Población en binario:")
        for ind in poblacion:
            print(f"x: {ind[0]}, y: {ind[1]}, z: {ind[2]}")
        
        # Evaluar población
        fitness = evaluar_poblacion(poblacion, bounds)
        print("Fitness:", fitness)
        
        nueva_poblacion = []
        
        # Selección y cruzamiento
        for _ in range(pop_size // 2):
            padre1 = seleccion_torneo(poblacion, fitness)
            padre2 = seleccion_torneo(poblacion, fitness)
            hijo1, hijo2 = cruzamiento_binario(padre1, padre2)
            
            # Mutación
            hijo1 = mutacion(hijo1)
            hijo2 = mutacion(hijo2)
            
            nueva_poblacion.extend([hijo1, hijo2])
        
        # Reemplazar la población
        poblacion = nueva_poblacion
    
    # Evaluar la población final
    fitness_final = evaluar_poblacion(poblacion, bounds)
    mejor_individuo = poblacion[fitness_final.index(max(fitness_final))]
    
    print("\nMejor individuo en binario:")
    print(f"x: {mejor_individuo[0]}, y: {mejor_individuo[1]}, z: {mejor_individuo[2]}")
    return mejor_individuo

def algoritmo_genetico_json(bounds, pop_size=4, generaciones=10, bits=5):
    # Inicializar población
    poblacion = [[generar_individuo(bounds, bits) for _ in range(3)] for _ in range(pop_size)]

    generations = []

    for gen in range(generaciones):
        fitness = evaluar_poblacion(poblacion, bounds)
        generacion_data = {"generacion": gen + 1, "poblacion": poblacion, "fitness": fitness}

        generations.append(generacion_data)

        nueva_poblacion = []

        # Selección y cruzamiento
        for _ in range(pop_size // 2):
            padre1 = seleccion_torneo(poblacion, fitness)
            padre2 = seleccion_torneo(poblacion, fitness)
            hijo1, hijo2 = cruzamiento_binario(padre1, padre2)

            # Mutación
            hijo1 = mutacion(hijo1)
            hijo2 = mutacion(hijo2)

            nueva_poblacion.extend([hijo1, hijo2])

        # Reemplazar la población
        poblacion = nueva_poblacion

    resultados = {
        "generaciones": generations
    }

    # Evaluar la población final
    fitness_final = evaluar_poblacion(poblacion, bounds)
    mejor_individuo = poblacion[fitness_final.index(max(fitness_final))]

    # Agregar mejor individuo como un atributo separado
    resultados["mejor_individuo"] = {
        "binario": mejor_individuo,
        "fitness": max(fitness_final)
    }

    return resultados

if __name__ == "__main__":
    bounds = [-10, 10]
    print(algoritmo_genetico_json(bounds))
