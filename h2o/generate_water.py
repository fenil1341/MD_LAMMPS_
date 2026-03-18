import numpy as np

# Box dimensions (Angstroms)
Lx = 100.0
Ly = 30.0
Lz = 30.0

n_molecules = 100

# SPC/E geometry
r_OH  = 1.0
half  = np.radians(109.47 / 2.0)
Hx    = r_OH * np.sin(half)
Hy    = r_OH * np.cos(half)

np.random.seed(42)

atoms  = []
bonds  = []
angles = []

for mol_id in range(1, n_molecules + 1):

    # Random position for oxygen, kept 2 Ang away from all walls
    ox = np.random.uniform(2.0, Lx - 2.0)
    oy = np.random.uniform(2.0, Ly - 2.0)
    oz = np.random.uniform(2.0, Lz - 2.0)

    # H positions relative to O
    h1x, h1y, h1z = ox - Hx, oy - Hy, oz
    h2x, h2y, h2z = ox + Hx, oy - Hy, oz

    base = (mol_id - 1) * 3
    id_O  = base + 1
    id_H1 = base + 2
    id_H2 = base + 3

    atoms.append((id_O,  mol_id, 1, -0.8476, ox,  oy,  oz ))
    atoms.append((id_H1, mol_id, 2,  0.4238, h1x, h1y, h1z))
    atoms.append((id_H2, mol_id, 2,  0.4238, h2x, h2y, h2z))

    bonds.append((len(bonds) + 1, 1, id_O, id_H1))
    bonds.append((len(bonds) + 1, 1, id_O, id_H2))

    angles.append((len(angles) + 1, 1, id_H1, id_O, id_H2))

with open("water_channel.data", "w") as f:
    f.write("LAMMPS water channel data file\n\n")
    f.write(f"{len(atoms)} atoms\n")
    f.write(f"{len(bonds)} bonds\n")
    f.write(f"{len(angles)} angles\n\n")
    f.write("2 atom types\n")
    f.write("1 bond types\n")
    f.write("1 angle types\n\n")
    f.write(f"0.0 {Lx:.4f} xlo xhi\n")
    f.write(f"0.0 {Ly:.4f} ylo yhi\n")
    f.write(f"0.0 {Lz:.4f} zlo zhi\n\n")
    f.write("Masses\n\n")
    f.write("1  15.9994  # Oxygen\n")
    f.write("2   1.0080  # Hydrogen\n\n")
    f.write("Atoms  # full\n\n")
    for a in atoms:
        f.write(f"{a[0]} {a[1]} {a[2]} {a[3]:.4f}  {a[4]:.6f}  {a[5]:.6f}  {a[6]:.6f}\n")
    f.write("\nBonds\n\n")
    for b in bonds:
        f.write(f"{b[0]} {b[1]} {b[2]} {b[3]}\n")
    f.write("\nAngles\n\n")
    for a in angles:
        f.write(f"{a[0]} {a[1]} {a[2]} {a[3]} {a[4]}\n")

print(f"Done. {n_molecules} molecules, {len(atoms)} atoms")
print("File written: water_channel.data")