import numpy as np
import matplotlib.pyplot as plt

# Beam parameters
beam_length = float(input("Enter beam length (m): "))

# Load input
num_point_loads = int(input("Enter number of point loads: "))
point_loads = []
for i in range(num_point_loads):
    magnitude = float(input(f"Point Load {i+1} magnitude (kN, positive down): "))
    position = float(input(f"Point Load {i+1} position from left support (m): "))
    point_loads.append((magnitude, position))

num_udls = int(input("Enter number of uniformly distributed loads (UDLs): "))
udls = []
for i in range(num_udls):
    magnitude = float(input(f"UDL {i+1} magnitude (kN/m): "))
    start = float(input(f"UDL {i+1} start position (m): "))
    end = float(input(f"UDL {i+1} end position (m): "))
    udls.append((magnitude, start, end))

# Calculate reactions at supports for simply supported beam (A at 0, B at L)
# Sum moments about A to find reaction at B:
moment_sum = 0.0
vertical_load_sum = 0.0
for load, pos in point_loads:
    vertical_load_sum += load
    moment_sum += load * pos

for magnitude, start, end in udls:
    length_udl = end - start
    load_total = magnitude * length_udl
    vertical_load_sum += load_total
    moment_sum += load_total * (start + length_udl / 2)

Rb = moment_sum / beam_length
Ra = vertical_load_sum - Rb

# Discretize beam length
x = np.linspace(0, beam_length, 500)
shear = np.zeros_like(x)
moment = np.zeros_like(x)

# Calculate shear force and bending moment at each segment
for i, xi in enumerate(x):
    V = Ra
    M = Ra * xi
    for load, pos in point_loads:
        if xi >= pos:
            V -= load
            M -= load * (xi - pos)
    for magnitude, start, end in udls:
        if xi >= start:
            length_seg = min(xi, end) - start
            if length_seg > 0:
                load_seg = magnitude * length_seg
                V -= load_seg
                M -= load_seg * (xi - (start + length_seg / 2))
    shear[i] = V
    moment[i] = M

# Plotting
plt.figure(figsize=(12,6))
plt.subplot(2,1,1)
plt.plot(x, shear, label='Shear Force (kN)')
plt.axhline(0, color='black', linewidth=0.5)
plt.title('Shear Force Diagram')
plt.ylabel('Shear Force (kN)')
plt.grid(True)
plt.legend()

plt.subplot(2,1,2)
plt.plot(x, moment, label='Bending Moment (kNm)', color='r')
plt.axhline(0, color='black', linewidth=0.5)
plt.title('Bending Moment Diagram')
plt.xlabel('Distance along beam (m)')
plt.ylabel('Bending Moment (kNm)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
