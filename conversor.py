import os
import sys

def convertir_txt_a_dat(txt_path, dat_path):
    """
    Convierte un archivo .txt en formato OR Library a un archivo .dat compatible con AMPL.
    """
    try:
        with open(txt_path, 'r') as file:
            lines = file.readlines()
        
        idx = 0  # Índice para recorrer las líneas
        total_lines = len(lines)
        
        # Función generadora para obtener líneas no vacías
        def line_gen():
            nonlocal idx
            while idx < total_lines:
                line = lines[idx].strip()
                idx += 1
                if line:  # Saltar líneas vacías
                    yield line
        
        generator = line_gen()
        
        # Leer m y n
        try:
            first_line = next(generator)
            m, n = map(int, first_line.split())
            print(f"Instancia encontrada: m={m}, n={n}")
        except StopIteration:
            raise ValueError("El archivo está vacío o no contiene m y n.")
        except ValueError:
            raise ValueError(f"Formato incorrecto en la primera línea: {first_line}")
        
        # Leer m líneas de almacenes
        almacenes = []
        for j in range(m):
            try:
                line = next(generator)
                parts = line.split()
                if len(parts) != 2:
                    raise ValueError(f"Línea {j+2}: Se esperaban 2 valores (capacidad y costo fijo), encontrados: {line}")
                capacidad = int(parts[0])
                costo_fijo = float(parts[1])
                almacenes.append((capacidad, costo_fijo))
            except StopIteration:
                raise ValueError(f"Se esperaban {m} líneas de almacenes, pero el archivo terminó antes.")
            except ValueError as ve:
                raise ValueError(f"Error en la línea {j+2}: {ve}")
        
        # Leer n clientes
        clientes = []
        for i in range(n):
            try:
                # Leer demanda
                demanda_line = next(generator)
                demanda = int(demanda_line)
            except StopIteration:
                raise ValueError(f"Se esperaban {n} clientes, pero el archivo terminó antes.")
            except ValueError:
                raise ValueError(f"Línea de demanda del cliente {i+1} tiene un formato incorrecto: {demanda_line}")
            
            # Leer m costos de asignación
            costos = []
            while len(costos) < m:
                try:
                    cost_line = next(generator)
                    costos_part = cost_line.split()
                    costos_flotantes = [float(c) for c in costos_part]
                    costos.extend(costos_flotantes)
                except StopIteration:
                    raise ValueError(f"Cliente {i+1}: Se esperaban {m} costos de asignación, pero el archivo terminó antes.")
                except ValueError:
                    raise ValueError(f"Cliente {i+1}: Formato incorrecto en línea de costos: {cost_line}")
            
            if len(costos) > m:
                costos = costos[:m]  # Truncar si hay más de m costos
            clientes.append((demanda, costos))
        
        # Generar el archivo .dat en el orden {D, C}
        with open(dat_path, 'w') as dat_file:
            # Definir conjuntos C y D
            C = ' '.join([f"j{j+1}" for j in range(m)])
            D = ' '.join([f"i{j+1}" for j in range(n)])
            dat_file.write(f"set C := {C};\n")
            dat_file.write(f"set D := {D};\n\n")
            
            # Parámetro de Capacidad
            dat_file.write("param s :=\n")
            for j in range(m):
                dat_file.write(f"j{j+1} {almacenes[j][0]}\n")
            dat_file.write(";\n\n")
            
            # Parámetro de Costo Fijo
            dat_file.write("param f :=\n")
            for j in range(m):
                dat_file.write(f"j{j+1} {almacenes[j][1]}\n")
            dat_file.write(";\n\n")
            
            # Parámetro de Demanda
            dat_file.write("param demand :=\n")
            for j in range(n):
                dat_file.write(f"i{j+1} {clientes[j][0]}\n")
            dat_file.write(";\n\n")
            
            # Parámetro de Costos de Asignación en orden {D, C} (clientes, almacenes)
            dat_file.write("param c : ")
            dat_file.write(' '.join([f"j{j+1}" for j in range(m)]))
            dat_file.write(" :=\n")
            for i in range(n):
                costos_str = ' '.join(map(str, clientes[i][1]))
                dat_file.write(f"i{i+1} {costos_str}\n")
            dat_file.write(";\n")
        
        print(f"Archivo {dat_path} generado exitosamente.")
    except Exception as e:
        print(f"Error durante la conversión: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="Convertidor de archivos OR Library .txt a .dat para AMPL.")
    parser.add_argument('-i', '--input', type=str, required=True,
                        help="Ruta al archivo .txt de entrada.")
    
    args = parser.parse_args()
    
    # Verificar que el archivo de entrada exista
    if not os.path.exists(args.input):
        print(f"Error: El archivo de entrada '{args.input}' no existe.")
        sys.exit(1)
    
    # Asegurar que la carpeta datos_dat existe
    output_dir = "datos_dat"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generar el nombre del archivo de salida en datos_dat con extensión .dat
    input_filename = os.path.splitext(os.path.basename(args.input))[0]
    dat_path = os.path.join(output_dir, f"{input_filename}.dat")
    
    # Ejecutar la conversión
    try:
        convertir_txt_a_dat(args.input, dat_path)
    except Exception as e:
        print(f"Error durante la conversión: {e}")
        sys.exit(1)
