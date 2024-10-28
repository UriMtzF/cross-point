import random
import json

# Función objetivo
def funcion_max(x, y, z):
    """Función objetivo a maximizar."""
    return x ** 2 + (y / z)

# Función objetivo de minimización
def funcion_min(x, y, z):
    """Transformación a minimización usando el inverso de la función de maximización."""
    # Aseguramos que el denominador sea positivo para evitar división entre 0
    return 1 / (1 + funcion_max(x, y, z))

# Decodificar binario a entero
def binario_a_entero(binario, bounds):
    min_bound, max_bound = bounds
    decimal = int(binario, 2)
    return min_bound + (decimal / (2**len(binario) - 1)) * (max_bound - min_bound)

# Generar un individuo aleatorio en binario
def generar_individuo(bounds, bits=5):
    return ''.join([random.choice(['0', '1']) for _ in range(bits)])

# Evaluar la función objetivo para una población
def evaluar_poblacion(poblacion, bounds, modo="max"):
    fitness = []
    for ind in poblacion:
        x_bin, y_bin, z_bin = ind
        x = binario_a_entero(x_bin, bounds)
        y = binario_a_entero(y_bin, bounds)
        z = binario_a_entero(z_bin, bounds)
        if z == 0:  # Evitar la división entre 0
            z = 1
        fitness.append(funcion_max(x, y, z) if modo == "max" else funcion_min(x, y, z))
    return fitness

# Selección por torneo
def seleccion_torneo(poblacion, fitness, k=2):
    participantes = random.sample(list(enumerate(fitness)), k)
    ganador = max(participantes, key=lambda x: x[1])
    return poblacion[ganador[0]], ganador

# Cruzamiento de un punto
def cruzamiento_binario(padre1, padre2):
    if len(padre1) != 3 or len(padre2) != 3:
        print(f"Error: padre1 o padre2 no tienen tres componentes. padre1: {padre1}, padre2: {padre2}")
        raise ValueError("Error en cruzamiento: los individuos no tienen la longitud correcta")
    punto_cruce = random.randint(1, len(padre1[0]) - 1)  # Usamos la longitud de cualquier cadena binaria
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

# Algoritmo genético consolidado
def algoritmo_genetico_json(bounds, pop_size=4, generaciones=10, bits=5):
    # Inicializar población
    poblacion = [[generar_individuo(bounds, bits) for _ in range(3)] for _ in range(pop_size)]
    generations = []

    for gen in range(generaciones):
        # Evaluar fitness para maximización y minimización
        fitness_max = evaluar_poblacion(poblacion, bounds, modo="max")
        fitness_min = evaluar_poblacion(poblacion, bounds, modo="min")

        generacion_data = {
            "generacion": gen + 1,
            "poblacion": poblacion,
            "fitness_max": fitness_max,
            "fitness_min": fitness_min,
            "competencias": []
        }

        nueva_poblacion = []

        # Selección y cruzamiento
        for _ in range(pop_size // 2):
            padre1, comp1 = seleccion_torneo(poblacion, fitness_max)  # Selección en maximización
            padre2, comp2 = seleccion_torneo(poblacion, fitness_max)
            ganador = padre1 if comp1[1] >= comp2[1] else padre2

            generacion_data["competencias"].append({
                "padre1": padre1,
                "padre2": padre2,
                "ganador": ganador
            })

            hijo1, hijo2 = cruzamiento_binario(padre1, padre2)
            hijo1 = mutacion(hijo1)
            hijo2 = mutacion(hijo2)
            nueva_poblacion.extend([hijo1, hijo2])

        poblacion = nueva_poblacion
        generations.append(generacion_data)

    # Evaluar el mejor individuo en ambos modos
    fitness_final_max = evaluar_poblacion(poblacion, bounds, modo="max")
    fitness_final_min = evaluar_poblacion(poblacion, bounds, modo="min")
    mejor_individuo_max = poblacion[fitness_final_max.index(max(fitness_final_max))]
    mejor_individuo_min = poblacion[fitness_final_min.index(min(fitness_final_min))]

    resultados = {
        "generaciones": generations,
        "mejor_individuo_max": {
            "binario": mejor_individuo_max,
            "fitness": max(fitness_final_max)
        },
        "mejor_individuo_min": {
            "binario": mejor_individuo_min,
            "fitness": min(fitness_final_min)
        }
    }

    return resultados


if __name__ == "__main__":
    bounds = [-10, 10]
    print(json.dumps(algoritmo_genetico_json(bounds, modo="max"), indent=2))
