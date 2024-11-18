def imprimir_y_exportar_lineas_personalizadas(ruta_archivo, ruta_salida):
    try:
        # Abrir el archivo en modo lectura
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()

        # Obtener las líneas especificadas
        max_index = len(lineas)
        indices = []

        # Generar el patrón solicitado
        for i in range(2002, max_index, 1):
            if i <= max_index:
                indices.append(i)
                indices.append(i + 2000)

        # Abrir el archivo de salida en modo escritura
        with open(ruta_salida, 'w', encoding='utf-8') as salida:
            # Imprimir las líneas correspondientes y exportarlas al archivo
            for idx in indices:
                if idx - 1 < max_index:  # Verificar que el índice esté dentro del rango
                    linea = lineas[idx - 1].strip()  # idx - 1 porque la lista es 0-based
                    print(linea)
                    salida.write(f"{linea}\n")  # Escribir en el archivo de salida

        print(f"El resultado se exportó correctamente a '{ruta_salida}'.")
    except FileNotFoundError:
        print(f"El archivo '{ruta_archivo}' no se encontró.")
    except Exception as e:
        print(f"Se produjo un error: {e}")

# Ruta del archivo de entrada y salida
ruta_entrada = "instancias/2000x2000_1.txt"
ruta_salida = "output.txt"

# Llamada a la función
imprimir_y_exportar_lineas_personalizadas(ruta_entrada, ruta_salida)
