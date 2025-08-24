import math
import matplotlib.pyplot as plt

print("=== Projectile Motion with Air Resistance Simulator ===")

try:
    # Inputs (wrapped inside try)
    u = float(input("Enter initial velocity (m/s): "))
    theta = float(input("Enter launch angle (degrees): "))

    # Check for negative values
    if u <= 0 or theta <= 0:
        raise ValueError("Invalid data: Velocity and angle must be positive numbers.")

except ValueError as e:
    # This will catch if user types string, space, or negative number
    print("Error:", e)
    print("Please enter only positive numbers (no letters, no spaces).")
    
else:
    # Constants
    g = 9.81         # gravity (m/s^2)
    rho = 1.225      # air density (kg/m^3)
    Cd = 0.47        # drag coefficient (sphere approx)
    A = 0.01         # cross-sectional area (m^2)
    m = 0.145        # mass (kg, like baseball)

    # Conversions
    theta_rad = math.radians(theta)

    # Initial velocities using math.sin and math.cos
    vx = u * math.cos(theta_rad)
    vy = u * math.sin(theta_rad)

    # Time step
    dt = 0.01
    x, y = 0.0, 0.0
    X, Y = [x], [y]

    max_height = 0.0

    while y >= 0.0:  # until projectile hits ground
        v = math.sqrt(vx**2 + vy**2)
        Fd = 0.5 * Cd * rho * A * v**2  # drag force
        ax = -(Fd/m) * (vx/v)
        ay = -(Fd/m) * (vy/v) - g
        
        # Update velocity
        vx += ax * dt
        vy += ay * dt
        
        # Update position
        x += vx * dt
        y += vy * dt
        
        if y > max_height:
            max_height = y  # track maximum height
        
        # Save for plotting
        X.append(x)
        Y.append(y)

    # Print results
    print("\n=== Results ===")
    print(f"Range: {x:.2f} m")
    print(f"Maximum Height: {max_height:.2f} m")
    print(f"Flight Time: {len(X)*dt:.2f} s")

    # Plotting
    plt.figure(figsize=(8,5))
    plt.plot(X, Y, label="With Air Resistance", color="red")
    plt.title("Projectile Motion with Air Resistance")
    plt.xlabel("Distance (m)")
    plt.ylabel("Height (m)")
    plt.legend()
    plt.grid(True)
    plt.show()

