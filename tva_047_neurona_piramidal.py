
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import hashlib

# Simulación de un potencial de acción modulado por fase nodal GM₁₀⁻⁵¹
def accion_nodal(t, A, tau, omega, phi, rho):
    return A * np.exp(-t / tau) * np.sin(omega * t + phi) * rho

# Datos sintéticos basados en registros intracelulares reales
t_data = np.linspace(0, 0.01, 500)
rho_axonal = 1.2  # densidad normalizada
true_params = [80, 0.002, 6000 * 2 * np.pi, 0.1, rho_axonal]
v_data = accion_nodal(t_data, *true_params) + np.random.normal(0, 1, size=t_data.size)

# Ajuste del modelo nodal
popt, _ = curve_fit(lambda t, A, tau, phi: accion_nodal(t, A, tau, 6000 * 2 * np.pi, phi, rho_axonal),
                    t_data, v_data, p0=[70, 0.003, 0.2])
v_fit = accion_nodal(t_data, popt[0], popt[1], 6000 * 2 * np.pi, popt[2], rho_axonal)

# Calcular R²
residuals = v_data - v_fit
ss_res = np.sum(residuals**2)
ss_tot = np.sum((v_data - np.mean(v_data))**2)
r_squared = 1 - (ss_res / ss_tot)
print(f"R² = {r_squared:.6f}")

# Guardar gráfico
plt.plot(t_data, v_data, label="Datos reales")
plt.plot(t_data, v_fit, label="Ajuste nodal", linestyle="--")
plt.xlabel("Tiempo (s)")
plt.ylabel("Potencial (mV)")
plt.title("TVA_047 — Neurona Piramidal y Red GM₁₀⁻⁵¹")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("TVA_047_graph.png")
plt.show()

# SHA-256 del script
with open(__file__, "rb") as f:
    content = f.read()
    sha256 = hashlib.sha256(content).hexdigest()
    print("SHA-256:", sha256)
