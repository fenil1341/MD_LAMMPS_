import re
import matplotlib.pyplot as plt
import numpy as np

# Read the log file
log_file = "log.lammps"
steps = []
poteng = []
KinEng = []

with open(log_file, 'r') as f:
    lines = f.readlines()

# Find the data section (starts after "Step          Temp          TotEng         PotEng...")
data_started = False
for line in lines:
    # Check if this is the header line
    if "Step" in line and "TotEng" in line and "PotEng" in line:
        data_started = True
        continue
    
    # Parse data lines
    if data_started:
        # Skip empty lines
        if not line.strip():
            continue
        
        # Try to parse the line as data
        parts = line.split()
        if len(parts) >= 4:
            try:
                # Extract Step (1st column) and PotEng (4th column)
                step = 0.001*int(parts[0])
                poteng_val = float(parts[3])
                KinEng_val = float(parts[4])
                steps.append(0.001*step)
                poteng.append(poteng_val)
                KinEng.append(KinEng_val)
            except (ValueError, IndexError):
                # Skip lines that don't contain numeric data
                continue

# # Create the plot
# plt.figure(figsize=(8, 6))
# plt.plot(steps, poteng, 'b-o', linewidth=1.5, markersize=2)
# plt.xlabel('time(ps)', fontsize=12)
# plt.ylabel('Potential Energy', fontsize=12)
# plt.title('Potential Energy vs time', fontsize=14)
# plt.grid(True, alpha=0.3)
# plt.tight_layout()

# Create the plot
plt.figure(figsize=(8, 6))
plt.plot(steps, KinEng, 'b-o', linewidth=1.5, markersize=2)
plt.xlabel('time(ps)', fontsize=12)
plt.ylabel('Kinetic Energy', fontsize=12)
plt.title('Kinetic Energy vs time', fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()



# # Save the plot
# plt.savefig('poteng_vs_step.png', dpi=300, bbox_inches='tight')
# print(f"Plot saved as 'poteng_vs_step.png'")
# print(f"Total data points: {len(steps)}")
# print(f"Step range: {steps[0]} to {steps[-1]}")
# print(f"PotEng range: {min(poteng):.2f} to {max(poteng):.2f}")

# Show the plot
plt.show()
# plt.savefig()