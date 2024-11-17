from amplpy import AMPL, Environment
import os
import sys
from ILS import iterated_local_search
import numpy as np
import pandas as pd


def ejecutar_modelo_ampl(mod_path, dat_path, solver='gurobi', max_nodes=None, time_limit=None):
    """
    Ejecutamos un modelo AMPL con los archivos .mod y .dat proporcionados,
    utilizando una heurística Iterated Local Search (ILS) para la solución inicial.

    Parámetros:
    - mod_path: Ruta al archivo .mod.
    - dat_path: Ruta al archivo .dat.
    - solver: Nombre del solver a utilizar (por defecto, 'gurobi').
    - max_nodes: Número máximo de nodos para el solver (opcional).
    - time_limit: Límite de tiempo para el solver (en segundos().
    """
    try:
        # Inicializamos AMPL
        ampl = AMPL(Environment())
        
        # Cargamos el modelo y los datos
        ampl.read(mod_path)
        ampl.readData(dat_path)
        
        # Extraemos parámetros y conjuntos para la heurística
        C = [j for j in ampl.getSet('C')]  # Conjunto de almacenes
        D = [i for i in ampl.getSet('D')]  # Conjunto de clientes
        
        # Extraemos parámetros asegurando que coincidan con las definiciones en AMPL
        s = {j: ampl.getParameter('s')[j] for j in C}  # Capacidades
        f = {j: ampl.getParameter('f')[j] for j in C}  # Costos fijos
        c = {i: {j: ampl.getParameter('c')[i, j] for j in C} for i in D}  # Costos de asignación
        demand_array = [ampl.getParameter('demand')[i] for i in D]  # Demandas
        
        # Convertimos parámetros a arrays para la heurística
        facilities = len(C)
        demand_total = sum(demand_array)
        
        # Creamos el array de capacidades y costos fijos
        cap_cost_array = np.zeros((facilities, 2))
        for idx, j in enumerate(C):
            cap_cost_array[idx, 0] = s[j]
            cap_cost_array[idx, 1] = f[j]
        
        # Crear la matriz de costos de asignación [clientes x centros]
        cost_matrix = np.zeros((len(D), len(C)))
        for i_idx, i in enumerate(D):
            for j_idx, j in enumerate(C):
                cost_matrix[i_idx, j_idx] = c[i][j]
        
        # Aplicamos la heurística ILS
        best_solution, best_fitness = iterated_local_search(
            cap_cost_array, demand_array, facilities, demand_total, cost_matrix
        )
        
        print("\n---EXACTO")
        print(f"Centros abiertos (como indices): {best_solution}")
        print(f"Centros abiertos (como nombres): {[f"j{i+1}" for i in best_solution]}")
        print(f"Costo: {best_fitness}")
        
        # Configuramos los centros abiertos en AMPL basados en la solución de ILS
        y = ampl.getVariable('y')
        for idx, j in enumerate(C):
            if idx in best_solution:
                y[j].fix(1)  # Fijar el valor de y[j] a 1 si el centro está abierto
            else:
                y[j].fix(0)  # Fijar el valor de y[j] a 0 si el centro está cerrado
        
        # Configuramos las asignaciones iniciales en AMPL
        x = ampl.getVariable('x')
        for i_idx, i in enumerate(D):
            for j_idx, j in enumerate(C):
                if j_idx in best_solution:
                    # Asignamos proporcionalmente la demanda
                    x[i, j].setValue(demand_array[i_idx] / len(best_solution))
                else:
                    x[i, j].setValue(0)

        # Configuramos el solver
        ampl.setOption('solver', solver)

        # Establecemos un criterio de término basado en nodos máximos o tiempo límite
        gurobi_options = 'MIPGap=1e-4'

        if time_limit is not None:
            gurobi_options += f' TimeLimit={time_limit}'

        if max_nodes is not None:
            gurobi_options += f' NodeLimit={max_nodes}'

        ampl.setOption('gurobi_options', gurobi_options)
        
        # Resolvemos el modelo
        ampl.solve()
        
        print(f"Resolviendo...")
        
        # Obtenemos valores de las variables
        y_values = ampl.getVariable("y").getValues().to_pandas()
        x_values = ampl.getVariable("x").getValues().to_pandas()
        
        # Obtener el valor de la función objetivo "TotalCost"
        total_cost_final = ampl.getObjective("TotalCost").value()
        print(f"Costo total final después de resolver el modelo: {total_cost_final}")

        # Mostramos los centros abiertos
        print("\nCentros abiertos:")
        for j in C:
            index = j  # Aquí, j debe coincidir con los índices como 'j1', 'j2', etc.
            valor = y_values.loc[index, 'y.val']  # Accedemos al valor correcto
            if valor > 0.5:
                print(f"{j}")

        # Mostramos las asignaciones de clientes
        print("\nAsignaciones de clientes:")
        for i in D:
            for j in C:
                index = (i, j)  # Índices como ('i1', 'j1')
                asignacion = x_values.loc[index, 'x.val']  # Accedemos al valor correcto
                if asignacion > 0:
                    print(f"Cliente {i} asignado a Centro {j}, con un costo de asignación: {asignacion}")
        
        print("\n--- COMPARACIÓN DE COSTOS ---")
        print(f"Costo inicial generado por ILS: {best_fitness}")
        print(f"Costo final optimizado por AMPL: {total_cost_final}")

    except Exception as e:
        print(f"Error al ejecutar el modelo AMPL: {e}")


if __name__ == "__main__":
    import argparse
    
    # Configuramos argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="Ejecutamos modelo AMPL con archivos .mod y .dat, utilizando una heurística Iterated Local Search (ILS) para la solución inicial.")
    parser.add_argument('-m', '--model', type=str, default='CFLP.mod',
                        help="Ruta al archivo .mod (por defecto: 'CFLP.mod').")
    parser.add_argument('-d', '--data', type=str, required=True, default=None,
                        help="Ruta al archivo .dat")
    parser.add_argument('-s', '--solver', type=str, default='gurobi',
                        help="Nombre del solver a utilizar (por defecto, 'gurobi').")
    parser.add_argument('-n', '--nodes', type=int, default=None,
                        help="Número máximo de nodos para el solver (opcional).")
    parser.add_argument('-t', '--time', type=int, default=None,
                        help="Límite de tiempo para el solver")
    
    args = parser.parse_args()
    
    # Verificamos que los archivos existan
    if not os.path.exists(args.model):
        print(f"Error: El archivo de modelo '{args.model}' no existe.")
        sys.exit(1)
    if not os.path.exists(args.data):
        print(f"Error: El archivo de datos '{args.data}' no existe.")
        sys.exit(1)
    
    # Ejecutamos el modelo
    ejecutar_modelo_ampl(args.model, args.data, args.solver, args.nodes, args.time)

