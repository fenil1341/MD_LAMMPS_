import numpy as np
import matplotlib.pyplot as plt

# Read energy.txt
timesteps = []
KE = []
PE = []

with open(r'F:\sla_hiwi\lammps_testRuns\steadyStateTest\waterOnly\waterOnly_small\without_force\energy.txt', 'r') as f:
    lines = f.readlines()

step = 0
for line in lines:
    line = line.strip()
    if line.startswith('#') or line == '':
        continue
    parts = line.split()
    if len(parts) == 2:
        try:
            KE.append(float(parts[0]))
            PE.append(float(parts[1]))
            timesteps.append(step)
            step += 1000
        except:
            continue


natoms = 750
timesteps = np.array(timesteps)
time_ps = timesteps * 1 / 1000
KE = np.array(KE)/natoms
PE = np.array(PE)/natoms


base_path = r'F:\sla_hiwi\lammps_testRuns\steadyStateTest\waterOnly\waterOnly_small\without_force'

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Water Only - No Force (Steady State Check)', fontsize=15)

# KE vs Timestep
axes[0, 0].plot(timesteps, KE, color='blue', linewidth=1)
axes[0, 0].set_xlabel('Timestep', fontsize=11)
axes[0, 0].set_ylabel('Kinetic Energy (kcal/mol/atom)', fontsize=11)
axes[0, 0].set_title('KE vs Timestep', fontsize=12)
axes[0, 0].grid(True, alpha=0.3)


# PE vs Timestep
axes[1, 0].plot(time_ps, KE, color='red', linewidth=1)
axes[1, 0].set_xlabel('Timestep', fontsize=11)
axes[1, 0].set_ylabel('Kinetic Energy (kcal/mol/atom)', fontsize=11)
axes[1, 0].set_title('KE vs Timestep', fontsize=12)
axes[1, 0].grid(True, alpha=0.3)


# PE vs Time
axes[0, 1].plot(timesteps, PE, color='blue', linewidth=1)
axes[0, 1].set_xlabel('Time (ps)', fontsize=11)
axes[0, 1].set_ylabel('Potential Energy (kcal/mol/atom)', fontsize=11)
axes[0, 1].set_title('PE vs Time', fontsize=12)
axes[0, 1].grid(True, alpha=0.3)


# PE vs Time
axes[1, 1].plot(time_ps, PE, color='red', linewidth=1)
axes[1, 1].set_xlabel('Time (ps)', fontsize=11)
axes[1, 1].set_ylabel('Potential Energy (kcal/mol/atom)', fontsize=11)
axes[1, 1].set_title('PE vs Time', fontsize=12)
axes[1, 1].grid(True, alpha=0.3)


# Plot Limits
# axes[0, 0].set_ylim(0, 1)    # KE vs Timestep
# axes[1, 0].set_ylim(0, 1)   # KE vs Timestep
# axes[0, 1].set_ylim(-5, -3)    # PE vs Time
# axes[1, 1].set_ylim(-5, -3)   # PE vs Time

plt.tight_layout()
plt.savefig(base_path + r'\energy_plots.png', dpi=150)
plt.show()

print("Done! Saved energy_plots.png")