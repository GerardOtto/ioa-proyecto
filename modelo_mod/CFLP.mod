# Definición de conjuntos
set C; # Conjunto de almacenes
set D; # Conjunto de clientes

# Definición de parámetros
param s{C}; # Capacidad de cada almacén
param f{C}; # Costo fijo de abrir cada almacén
param demand{D}; # Demanda de cada cliente
param c{D, C}; # Costo de asignar cliente j a almacén i

# Definición de variables
var y{C} binary; # y[j] = 1 si se abre el almacén j, 0 en caso contrario
var x{D, C} >= 0; # Cantidad de demanda del cliente i asignada al almacén j

# Función objetivo: Minimizar costos totales
minimize TotalCost:
    sum {j in C} f[j] * y[j] + sum {i in D, j in C} c[i, j] * x[i, j];

# Restricciones

# Cada cliente debe ser completamente atendido
subject to AssignDemand {i in D}:
    sum {j in C} x[i, j] >= demand[i];

# No exceder la capacidad de los almacenes
subject to CapacityLimit {j in C}:
    sum {i in D} x[i, j] <= s[j] * y[j];
