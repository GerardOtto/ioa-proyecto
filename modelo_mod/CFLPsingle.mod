# Definición de conjuntos
set C; # Conjunto de almacenes
set D; # Conjunto de clientes

# Definición de parámetros
param s{C}; # Capacidad de cada almacén
param f{C}; # Costo fijo de abrir cada almacén
param demand{D}; # Demanda de cada cliente
param c{D, C}; # Costo de asignar cliente i al almacén j

# Definición de variables
var y{C} binary; # y[j] = 1 si se abre el almacén j, 0 en caso contrario
var x{D, C} binary; # x[i, j] = 1 si el cliente i es asignado al almacén j, 0 en caso contrario

# Función objetivo: Minimizar costos totales
minimize TotalCost:
    sum {j in C} f[j] * y[j] + sum {i in D, j in C} c[i, j] * x[i, j];

# Restricciones

# Cada cliente debe ser atendido por exactamente un almacén
subject to SingleSource {i in D}:
    sum {j in C} x[i, j] = 1;

# La capacidad de los almacenes no debe ser excedida
subject to CapacityLimit {j in C}:
    sum {i in D} demand[i] * x[i, j] <= s[j] * y[j];

# No se puede asignar un cliente a un almacén cerrado
subject to OpenFacility {i in D, j in C}:
    x[i, j] <= y[j];