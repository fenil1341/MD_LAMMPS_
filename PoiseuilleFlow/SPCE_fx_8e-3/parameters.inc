mass O 15.9994
mass H 1.008
mass WALL 26.9815
mass Na+ 22.990
mass Cl- 35.453

# pair_style lj/cut/coul/cut 10.0
pair_coeff O O 0.1553 3.166
pair_coeff O H 0.0    1.0
pair_coeff H H 0.0    1.0
pair_coeff WALL WALL 11.697 2.574
pair_coeff O WALL 0.4 2.86645
pair_coeff Na+ Na+ 0.04690 2.4299
pair_coeff Cl- Cl- 0.1500 4.04470


bond_coeff 1 450 1.0
angle_coeff 1 55 109.47