import numpy as np
import matplotlib.pyplot as plt

# Read energy.txt
timesteps = []
KE = []
PE = []
Temp = []

with open(r'F:\sla_hiwi\lammps_testRuns\steadyStateTest\water_KCl\energy.txt', 'r') as f:
    lines = f.readlines()

for line in lines:
    line = line.strip()
    if line.startswith('#') or line == '':
        continue
    parts = line.split()
    if len(parts) == 4:
        try:
            timesteps.append(float(parts[0]))
            KE.append(float(parts[1]))
            PE.append(float(parts[2]))
            Temp.append(float(parts[3]))
        except:
            continue
ts = 0.1
natoms = 760
timesteps = np.array(timesteps)
time_ps = timesteps * ts / 1000
KE = np.array(KE) / natoms
PE = np.array(PE) / natoms
Temp = np.array(Temp)

base_path = r'F:\sla_hiwi\lammps_testRuns\steadyStateTest\water_KCl'

fig, axes = plt.subplots(3, 2, figsize=(6, 8))
fig.suptitle('Water + Ions - No Force (Steady State Check) \n Energy in (kcal/mol/atom)', fontsize=15)

# KE vs Timestep
axes[0, 0].plot(timesteps, KE, color='blue', linewidth=1)
axes[0, 0].set_xlabel('Timestep', fontsize=11)
axes[0, 0].set_ylabel('KE ', fontsize=11)
axes[0, 0].set_title('KE vs Timestep', fontsize=12)
axes[0, 0].grid(True, alpha=0.3)

# KE vs Time
axes[1, 0].plot(time_ps, KE, color='blue', linewidth=1)
axes[1, 0].set_xlabel('Time (ps)', fontsize=11)
axes[1, 0].set_ylabel('KE', fontsize=11)
axes[1, 0].set_title('KE vs Time', fontsize=12)
axes[1, 0].grid(True, alpha=0.3)

# PE vs Timestep
axes[0, 1].plot(timesteps, PE, color='red', linewidth=1)
axes[0, 1].set_xlabel('Timestep', fontsize=11)
axes[0, 1].set_ylabel('PE', fontsize=11)
axes[0, 1].set_title('PE vs Timestep', fontsize=12)
axes[0, 1].grid(True, alpha=0.3)

# PE vs Time
axes[1, 1].plot(time_ps, PE, color='red', linewidth=1)
axes[1, 1].set_xlabel('Time (ps)', fontsize=11)
axes[1, 1].set_ylabel('PE', fontsize=11)
axes[1, 1].set_title('PE vs Time', fontsize=12)
axes[1, 1].grid(True, alpha=0.3)

# Temp vs Timestep
axes[2, 0].plot(timesteps, Temp, color='green', linewidth=1)
axes[2, 0].set_xlabel('Timestep', fontsize=11)
axes[2, 0].set_ylabel('Temperature (K)', fontsize=11)
axes[2, 0].set_title('Temperature vs Timestep', fontsize=12)
axes[2, 0].axhline(y=300, color='black', linestyle='--', label='Target 300K')
axes[2, 0].legend()
axes[2, 0].grid(True, alpha=0.3)
axes[2, 0].set_ylim(200, 400)

# Temp vs Time
axes[2, 1].plot(time_ps, Temp, color='green', linewidth=1)
axes[2, 1].set_xlabel('Time (ps)', fontsize=11)
axes[2, 1].set_ylabel('Temperature (K)', fontsize=11)
axes[2, 1].set_title('Temperature vs Time', fontsize=12)
axes[2, 1].axhline(y=300, color='black', linestyle='--', label='Target 300K')
axes[2, 1].legend()
axes[2, 1].grid(True, alpha=0.3)
axes[2, 1].set_ylim(200, 400)

plt.tight_layout()
plt.savefig(base_path + r'\energy_plots.png', dpi=150)
plt.show()

print("Done! Saved energy_plots.png")