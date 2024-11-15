# Uso del Programa para una Instancia de Ejemplo

El flujo de ejecución del programa para una instancia de ejemplo `cap41.txt` se realiza de esta forma:

1. **Convertir el archivo `.txt` a un archivo `.dat`:**  
   Para que el algoritmo exacto pueda utilizar los datos, se ejecuta este comando en la terminal del directorio del proyecto:

   ```bash
   python conversor.py -i instancias/cap41.txt
   ```

2. **Cargar el `.dat` y el `.mod` para el algoritmo exacto:**  
   El algoritmo exacto necesita el .dat generado anteriormente. Utiliza una heurística ILS para encontrar una solución inicial y luego resuelve. Para ejecutarlo, usa el siguiente comando:

   ```bash
   python algoritmo_exacto.py -m CFLP.mod -d datos_dat/cap41.dat
   ```
