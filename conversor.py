import os
import sys

def convertir_txt_a_dat_mod(txt_path, dat_path):
    """
    Convierte un archivo .txt en formato OR Library a un archivo .dat compatible con el nuevo CFLP.mod.
    """
    try:
        with open(txt_path, 'r') as file:
            lines = file.readlines()
        
        idx = 0  # Índice para recorrer las líneas
        total_lines = len(lines)
        
        def line_gen():
            nonlocal idx
            while idx < total_lines:
                line = lines[idx].strip()
                idx += 1
                if line:  # Saltar líneas vacías
                    yield line
        
        generator = line_gen()
        
        # Leer m y n
        first_line = next(generator)
        m, n = map(int, first_line.split())
        print(f"Instancia encontrada: m={m}, n={n}")
        
        almacenes = []
        for _ in range(m):
            line = next(generator)
            capacidad, costo_fijo = map(float, line.split())
            almacenes.append((capacidad, costo_fijo))
        
        clientes = []
        for _ in range(n):
            demanda = float(next(generator))
            costos = []
            while len(costos) < m:
                costos.extend(map(float, next(generator).split()))
            clientes.append((demanda, costos))
        
        with open(dat_path, 'w') as dat_file:
            # Definir conjuntos
            C = ' '.join([f"j{j+1}" for j in range(m)])
            D = ' '.join([f"i{i+1}" for i in range(n)])
            dat_file.write(f"set C := {C};\n")
            dat_file.write(f"set D := {D};\n\n")
            
            # Capacidad de almacenes
            dat_file.write("param s :=\n")
            for j in range(m):
                dat_file.write(f"j{j+1} {almacenes[j][0]}\n")
            dat_file.write(";\n\n")
            
            # Costo fijo de almacenes
            dat_file.write("param f :=\n")
            for j in range(m):
                dat_file.write(f"j{j+1} {almacenes[j][1]}\n")
            dat_file.write(";\n\n")
            
            # Demanda de clientes
            dat_file.write("param demand :=\n")
            for i in range(n):
                dat_file.write(f"i{i+1} {clientes[i][0]}\n")
            dat_file.write(";\n\n")
            
            # Costos de asignación
            dat_file.write("param c : ")
            dat_file.write(' '.join([f"j{j+1}" for j in range(m)]))
            dat_file.write(" :=\n")
            for i in range(n):
                dat_file.write(f"i{i+1} {' '.join(map(str, clientes[i][1]))}\n")
            dat_file.write(";\n")
        
        print(f"Archivo {dat_path} generado exitosamente.")
    except Exception as e:
        print(f"Error durante la conversión: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convertidor de archivos OR Library .txt a .dat para CFLP.mod.")
    parser.add_argument('-i', '--input', type=str, required=True, help="Ruta al archivo .txt de entrada.")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: El archivo de entrada '{args.input}' no existe.")
        sys.exit(1)

    output_dir = "datos_dat"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    input_filename = os.path.splitext(os.path.basename(args.input))[0]
    dat_path = os.path.join(output_dir, f"{input_filename}.dat")

    convertir_txt_a_dat_mod(args.input, dat_path)
