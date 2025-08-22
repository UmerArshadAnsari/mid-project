import matplotlib.pyplot as plt # as it will call only plot function
import math

print("=== Projectile Motion with Air Resistance Simulator ===")

# Inputs
u = float(input("Enter initial velocity (m/s): "))
theta = float(input("Enter launch angle (degrees): "))

# Constants
g = 9.81         # gravity (m/s^2)
rho = 1.225      # air density (kg/m^3)
Cd = 0.47        # drag coefficient (sphere approx)
A = 0.01         # cross-sectional area of sphere (m^2)
m = 0.145        # mass (kg, like baseball)

# Conversions
theta_rad = math.radians(theta)

# Initial velocities
vx = u * math.cos(theta_rad)
vy = u * math.sin(theta_rad)

# Time step
dt = 0.01
t = 0.0
x, y = 0, 0
X, Y = [x], [y]

max_height = 0.0   # track maximum height

while y >= 0:  
    v = math.sqrt(vx**2 + vy**2)          # speed magnitude
    Fd = 0.5 * Cd * rho * A * v**2        # drag force
    ax = -(Fd/m) * (vx/v)                 # acceleration x
    ay = -(Fd/m) * (vy/v) - g             # acceleration y (with gravity)
    
    # Update velocity
    vx += ax * dt
    vy += ay * dt
    
    # Update position
    x += vx * dt
    y += vy * dt
    t += dt   #time
    
    # Save for plot
    X.append(x)
    Y.append(y)
    
    # it will track maximum height
    if y > max_height:
        max_height = y

# Results
time_of_flight = t
range_proj = x
max_height = max_height

print("\n--- Results ---")
print(f"Time of Flight of sphere (seconds): {time_of_flight:.2f}")
print(f"Maximum Height of sphere(meter): {max_height:.2f}")
print(f"Horizontal Range of sphere (meter): {range_proj:.2f}")

# Plotting the graph
plt.figure(figsize=(50,40))
plt.plot(X, Y, label="With Air Resistance", color="red")
plt.title("Projectile Motion Simulation with Air Resistance")
plt.xlabel("Distance (m)")
plt.ylabel("Height (m)")
plt.legend()
plt.grid(True)
plt.show()

