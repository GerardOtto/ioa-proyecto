from amplpy import AMPL
import argparse

def ejecutar_ampl_con_gurobi(mod_path, dat_path):
    # Inicializar AMPL
    ampl = AMPL()

    # Configurar gurobi como solver
    ampl.option['solver'] = 'gurobi'

    # Leer el archivo de modelo (.mod)
    ampl.read(mod_path)

    # Leer el archivo de datos (.dat)
    ampl.readData(dat_path)

    # Resolver el problema
    try:
        ampl.solve()
        # Imprimir el estado de solución
        solve_status = ampl.getValue("solve_result")
        print(f"Estado de la solución: {solve_status}")

        # Imprimir el valor de la función objetivo
        objetivo = ampl.getObjective("TotalCost").value()
        print(f"Valor óptimo de la función objetivo: {objetivo}")

        # Opcional: Imprimir variables de decisión
        y = ampl.getVariable("y").getValues()
        x = ampl.getVariable("x").getValues()
        print("Valores de y:")
        print(y)
        print("Valores de x:")
        print(x)

    except Exception as e:
        print(f"Error al resolver el modelo: {e}")

if __name__ == "__main__":
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="Ejecuta un modelo AMPL con el solver HiGHS.")
    parser.add_argument('-m', '--modpath', type=str, required=True, help="Ruta al archivo .mod (modelo).")
    parser.add_argument('-d', '--datpath', type=str, required=True, help="Ruta al archivo .dat (datos).")

    args = parser.parse_args()

    # Ejecutar la función con los argumentos proporcionados
    ejecutar_ampl_con_gurobi(args.modpath, args.datpath)
