# Instancias:

**Pequeñas:** `cap41.txt`, `cap42.txt`

**Grandes:** `capb.txt`, `capc.txt`

# Parámetros de la terminal:

- **-m**: Ruta al archivo .mod (opcional, por defecto: CFLP.mod).
- **-d**: Ruta al archivo .dat generado (obligatorio).
- **-s**: Nombre del solver a utilizar (opcional, por defecto: gurobi).

**Criterios de término:**

- **-n**: Número máximo de nodos para el solver (opcional).
- **-t**: Límite de tiempo para el solver en segundos (opcional).

# Uso del programa para una instancia de ejemplo:

El flujo de ejecución del programa para una instancia de ejemplo `cap41.txt` se realiza de esta forma:

1. **Convertir el archivo `.txt` a un archivo `.dat`:**  
   Para que el algoritmo exacto pueda utilizar los datos, se ejecuta este comando en la terminal del directorio del proyecto:

   ```bash
   python conversor.py -i instancias/cap41.txt
   ```

2. **Cargar el `.dat` y el `.mod` para el algoritmo exacto:**  
   El algoritmo exacto necesita el .dat generado anteriormente. Utiliza una heurística ILS para encontrar una solución inicial y luego resuelve. Para ejecutarlo, usa el siguiente comando:

   ```bash
   python algoritmo_exacto.py -m modelo_mod/CFLP.mod -d datos_dat/cap41.dat -n 1000 -t 1200
   ```
