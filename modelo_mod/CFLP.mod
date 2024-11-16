# Definición de conjuntos
set C; # Conjunto de almacenes
set D; # Conjunto de clientes

# Definición de parámetros
param s{C}; # Capacidad de cada almacén
param f{C}; # Costo fijo de abrir cada almacén
param demand{D}; # Demanda de cada cliente
param c{D, C}; # Costo de asignar cliente j a almacén i

# Definición de variables
var y{C} binary; # y[i] = 1 si se abre el almacén i, 0 en caso contrario
var x{D, C} >= 0; # Cantidad de demanda del cliente j asignada al almacén i

# Función objetivo: Minimizar costos totales
minimize TotalCost:
    sum{j in C} f[j] * y[j] + sum{j in D, i in C} c[j, i] * x[j, i];

# Restricciones
# Cada cliente debe ser completamente atendido
subject to AssignDemand{j in D}:
    sum{i in C} x[j, i] >= demand[j];

# No exceder la capacidad de los almacenes
subject to CapacityLimit{i in C}:
    sum{j in D} x[j, i] <= s[i] * y[i];
