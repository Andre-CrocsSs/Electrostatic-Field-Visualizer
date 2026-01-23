import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm

def charge_factory(X, Y, xc, yc, q):
    # Componentes de distancia
    dx = X - xc
    dy = Y - yc

    # Ley de Coulomb
    rr = (dx ** 2) + (dy ** 2) + 1e-20
    r = np.sqrt(rr)

    # Campo eléctrico
    E_x = (k_v * q * dx) / (r ** 3)
    E_y = (k_v * q * dy) / (r ** 3)
    
    # Potencial eléctrico
    V = k_v * (q / r)
    return E_x, E_y, V

# Creo el tablero donde proyectaré el campo
x_list = np.linspace(-10, 10, 20)
y_list = np.linspace(-10, 10, 20)

X, Y = np.meshgrid(x_list, y_list)

Ex_total = np.zeros_like(X)
Ey_total = np.zeros_like(X)
V_total = np.zeros_like(X)
coords_x = []
coords_y = []

k_v = 9e9
charge_q = int(input("How many charges do you want to plot? "))

for i in range(charge_q):
    xc = float(input("What's the x coordinate of the charge? "))
    yc = float(input("What's the y coordinate of the charge? "))
    q = float(input("What's the charge intensity (in Coulombs)? "))
    
    E_x, E_y, V = charge_factory(X, Y, xc, yc, q)
    Ex_total = E_x + Ex_total
    Ey_total = E_y + Ey_total
    V_total = V + V_total
    coords_x.append(xc)
    coords_y.append(yc)

print("\n--- Visualization options ---")
print("1. Only potential map (colors)")
print("2. Only field lines (vectors)")
print("3. Combined mode (both)")
opt = input("Chose an option (1, 2 o 3): ")

# Comienzo la gráfica con plt
norm=SymLogNorm(linthresh=1, vmin=-1e10, vmax=1e10, base=10)

plt.figure(figsize=(12, 8))
# 1. Capa de Fondo (Potencial)
if opt == "1":
    mapa = plt.contourf(X, Y, V_total, levels=200, cmap='RdBu', norm=norm)
    plt.colorbar(mapa, label='Electric potential (V)')
    if charge_q == 1:
        plt.title(f"Electric Potential Map (a charge)")
    else:
        plt.title(f"Electric Potential Map ({charge_q} charges)")

# 2. Capa de Flujo (Campo Puro)
elif opt == "2":
    plt.streamplot(X, Y, Ex_total, Ey_total, color='black')
    if charge_q == 1:
        plt.title(f"Electric Field Lines (a charge)")
    else:
        plt.title(f"Electric Field Lines ({charge_q} charges)")

# 3. Modo Combinado
elif opt == "3":
    mapa = plt.contourf(X, Y, V_total, levels=200, cmap='RdBu', norm=norm)
    plt.colorbar(mapa, label='Electric potential (V)')
    plt.streamplot(X, Y, Ex_total, Ey_total, color='black')
    if charge_q == 1:
        plt.title(f"Full Electrostatic Analysis (a charge)")
    else:
        plt.title(f"Full Electrostatic Analysis ({charge_q} charges)")


# Dibujo cargas y leyenda (en todos)
for i in range(len(coords_x)):
    plt.scatter(coords_x[i], coords_y[i], label=f"Charge {i+1}", zorder=10, s=100)

plt.legend(bbox_to_anchor=(-0.15, 1), loc='upper right')
plt.tight_layout()
plt.show()
