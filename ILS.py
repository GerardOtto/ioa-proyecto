from collections import defaultdict
import random
import copy
import numpy as np

def solution_capacity(solution: list, cap_cost_array) -> float:
    """
    Calcula la capacidad total de una solución dada.
    
    Parámetros:
    - solution: Lista de índices de centros abiertos.
    - cap_cost_array: Array de capacidades y costos fijos de los centros.
    
    Retorna:
    - Capacidad total.
    """
    capacity = 0
    for center in solution:
        capacity += cap_cost_array[center, 0]
    return capacity

def solution_fitness(solution: list, cap_cost_array) -> float:
    """
    Calcula el costo total de una solución, incluyendo costos fijos de apertura.
    
    Parámetros:
    - solution: Lista de índices de centros abiertos.
    - cap_cost_array: Array de capacidades y costos fijos de los centros.
    
    Retorna:
    - Costo total.
    """
    fitness = 0
    
    # Sumar costos fijos de apertura
    for center in solution:
        fitness += cap_cost_array[center, 1]
    
    return fitness


def fix_solution(solution: list, demand: float, max_facility: int, cap_cost_array) -> list:
    """
    Ajusta una solución para asegurar que la capacidad total cubra la demanda total,
    añadiendo centros aleatorios si es necesario.
    
    Parámetros:
    - solution: Lista de índices de centros abiertos.
    - demand: Demanda total a cubrir.
    - max_facility: Número total de centros disponibles.
    - cap_cost_array: Array de capacidades y costos fijos de los centros.
    
    Retorna:
    - Solución ajustada.
    """
    current_capacity = solution_capacity(solution, cap_cost_array)

    # si se cumple la demanda
    if current_capacity >= demand:
        return solution
    # se añaden centros aleatorios
    while current_capacity < demand:
        new_center = random.randint(0, max_facility - 1)

        if new_center not in solution:
            solution.append(new_center)
            current_capacity += cap_cost_array[new_center, 0]

    return solution

def iterated_local_search(cap_cost_array, facilities, demand_total, global_iterations=5, time_intervals=None):
    """
    Implementación de la heurística Iterated Local Search (ILS) para CFLP.
    
    Parámetros:
    - cap_cost_array: Array de capacidades y costos fijos de los centros.
    - facilities: Número total de centros disponibles.
    - demand_total: Demanda total a cubrir.
    - global_iterations: Número de iteraciones globales.
    - time_intervals: Lista de intervalos de tiempo para iteraciones locales.
    
    Retorna:
    - best_solution: Lista de índices de centros abiertos de la mejor solución encontrada.
    - best_fitness: Costo total de la mejor solución.
    """
    if time_intervals is None:
        time_intervals = [10, 20, 30, 40, 50, 60, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
    
    # Solución inicial aleatoria
    initial_solution = []
    
    # Llenamos la lista con centros aleatorios hasta que la capacidad >= demanda
    while solution_capacity(initial_solution, cap_cost_array) < demand_total:
        center = random.randint(0, facilities - 1)
        if center not in initial_solution:
            initial_solution.append(center)
    
    print("--- ILS")
    print("La solución inicial:", initial_solution)
    print("El costo de apertura inicial:", solution_fitness(initial_solution, cap_cost_array))
    
    # La solución inicial es la mejor solución
    best_solution = copy.deepcopy(initial_solution)
    solution = copy.deepcopy(initial_solution)
    
    # Corremos el algoritmo la cantidad de global_iterations
    for i in range(global_iterations):
        # Seleccionamos un intervalo de tiempo aleatorio
        time = random.choice(time_intervals)
        
        # Realizamos cambios locales en la solución
        for j in range(time):
            tweaked_solution = copy.deepcopy(solution)
            
            # Realizamos una perturbación: cambiamos un centro aleatorio
            if len(tweaked_solution) == 0:
                continue
            tweaked_index = random.randint(0, len(tweaked_solution) - 1)
            old_center = tweaked_solution[tweaked_index]
            delta = random.randint(-3, 3)
            new_center = max(0, min(facilities - 1, old_center + delta))
            
            # Si el nuevo centro ya está en la solución, saltamos
            if new_center in tweaked_solution:
                continue
            else:
                tweaked_solution[tweaked_index] = new_center
            
            # Arreglamos la solución si es necesario
            if solution_capacity(tweaked_solution, cap_cost_array) < demand_total:
                tweaked_solution = fix_solution(tweaked_solution, demand_total, facilities, cap_cost_array)
            
            # Comparamos la solución tweaked con la actual
            tweaked_fitness = solution_fitness(tweaked_solution, cap_cost_array)
            current_fitness = solution_fitness(solution, cap_cost_array)
            
            if tweaked_fitness <= current_fitness:
                solution = copy.deepcopy(tweaked_solution)
        
        # Comparar y actualizar la mejor solución
        current_fitness = solution_fitness(solution, cap_cost_array)
        best_fitness = solution_fitness(best_solution, cap_cost_array)
        
        if current_fitness < best_fitness:
            best_solution = copy.deepcopy(solution)
        
        # Parte de random restart: crear una nueva solución
        new_base = []
        while solution_capacity(new_base, cap_cost_array) < demand_total:
            center = random.randint(0, facilities - 1)
            if center not in new_base:
                new_base.append(center)
        
        # Probabilidad de aceptar la nueva solución
        if solution_fitness(new_base, cap_cost_array) < solution_fitness(solution, cap_cost_array):
            solution = copy.deepcopy(new_base)
        elif random.random() < 0.15:
            solution = copy.deepcopy(new_base)
    
    print("La solución final es:", best_solution)
    print("El costo de apertura final es:", solution_fitness(best_solution, cap_cost_array))
    
    return best_solution, solution_fitness(best_solution, cap_cost_array)