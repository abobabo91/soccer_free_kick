import math
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle





#-----------------CALCULATIONS



def calculate_trajectory_params(goal_distance, wall_distance, wall_height):
    # constants
    goes_in_height= 2.25
    # 2.25 is the height for the bottom of the ball for the ball to go in
    # ~= 2.44 - 0.23 ----- goal height - ball size measured from the bottom! plus as much as it bounces in from the post
    
    g = 9.81                # gravitational acceleration (m/s^2)
    rho = 1.225             # air density (kg/m^3)
    r = 0.115                # approx. radius of soccer ball (m)
    A = math.pi * r * r     # cross-sectional area (m^2)
    m = 0.43                # mass of a typical soccer ball (kg)
    
    #May not to be changed according to field tests
    Cd = 0.25        # drag coefficient of a soccer ball (per NASA)
    
    # Quadratic drag factor k = (1/2)*(rho)*(Cd)*(A) / m
    k = 0.5 * rho * Cd * A / m
    
    initial_guess = (30.0, 20.0)  # (angle in degrees, velocity in m/s)
    solution = fsolve(equations, initial_guess)
    kick_angle_deg, launch_velocity_ms = solution
    
    max_kick_velocity_kmh = launch_velocity_ms * 3.6
    
    tangent_angle = math.tan(math.radians(kick_angle_deg))  # Calculate the tangent of the kick angle
    horizontal_velocity = launch_velocity_ms * math.cos(math.radians(kick_angle_deg))  # Horizontal velocity component
    time_to_reach_goal = goal_distance / horizontal_velocity  # Time to reach the goal


    return kick_angle_deg, launch_velocity_ms, max_kick_velocity_kmh, tangent_angle, horizontal_velocity, time_to_reach_goal


#-------------------------VISUALIZATION


def plot_trajectory(kick_angle_deg, launch_velocity_ms, max_kick_velocity_kmh, tangent_angle, horizontal_velocity, time_to_reach_goal):
    # Initial conditions
    angle_rad = math.radians(kick_angle_deg)
    vx0 = launch_velocity_ms * math.cos(angle_rad)
    vy0 = launch_velocity_ms * math.sin(angle_rad)
    
    state0 = [0.0, 0.0, vx0, vy0]  # (x=0, y=0, vx=vx0, vy=vy0)
    t_final = goal_distance / launch_velocity_ms * 2  # or however long you expect flight to last
    t_points = 50 
    t_span = np.linspace(0, t_final, t_points)
    
    solution = odeint(projectile_odes, state0, t_span)
    x_vals = solution[:, 0]
    y_vals = solution[:, 1]
    
    # ---------------------------------------------
    # 4) Plot: side-view of trajectory, wall, and goal
    # ---------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the ball as a circle at each time step
    # (For clarity, you might skip some points, e.g., step by 5)
    for i in range(len(x_vals)):
        center_x = x_vals[i]
        center_y = y_vals[i] + r
        # Draw a transparent circle representing the ball
        circle = Circle((center_x, center_y), radius=r,
                        fill=False, edgecolor='blue', alpha=0.5)
        ax.add_patch(circle)
    
    # Draw the wall as a vertical line from y=0 to y=wall_height
    ax.plot([wall_distance, wall_distance],
            [0, wall_height],
            color='red', linewidth=2, label='Wall')
    
    # Draw the goal: a rectangle at goal_distance, height=2.44 m
    goal_width = 0.2  # thickness of the "goal posts" in the plot
    goal_height = 2.44
    goal_rect = Rectangle((goal_distance, 0),
                          goal_width, goal_height,
                          fill=False, edgecolor='green', linewidth=2, label='Goal')
    ax.add_patch(goal_rect)
    
    vertical_positions = [2.5]
    
    # ---------------------------------------------
    # 5) Annotate: angle & velocity
    # ---------------------------------------------
    # Put some text near the origin or top-left corner

    plt.annotate(
        f"Angle: {kick_angle_deg:.2f}°",
        xy=(0, 0),
        xytext=(5, 0.5),
        arrowprops=dict(facecolor='black', arrowstyle="->"),
        fontsize=10,
        color="black"
    )
    
    plt.text(
        1, max(vertical_positions) - 0.5,
        f"Velocity: {max_kick_velocity_kmh:.2f}km/h",
        fontsize=10,
        color="blue"
    )
    
    plt.text(
        1, max(vertical_positions) - 0.3,
        f"Time to reach goal: {time_to_reach_goal:.2f}s",
        fontsize=10,
        color="blue"
    )
    plt.text(
        1, max(vertical_positions) + 0.3,
        f"Wall distance: {wall_distance:.2f}m",
        fontsize=10,
        color="red"
    )
    plt.text(
        1, max(vertical_positions) + 0.5,
        f"Goal distance: {goal_distance:.2f}m",
        fontsize=10,
        color="red"
    )
    
    # ---------------------------------------------
    # 6) Final plot adjustments
    # ---------------------------------------------
    # Set axis limits so we can see everything
    max_x = max(x_vals) + 2
    max_y = max(y_vals) + 1
    ax.set_xlim(0, max(goal_distance+2, 0))  # ensure we see goal
    ax.set_ylim(0, max( wall_height, goal_height, max_y ))
    
    ax.set_xlabel('Horizontal distance (m)')
    ax.set_ylabel('Height (m)')
    ax.set_title('Soccer Ball Trajectory with Drag')
    
    ax.grid(True)
    ax.legend(loc='upper right')
    
    plt.show()
    










#---------------------------EQUATIONS

# ---------------------------------------------
# 2) Define the ODE system with drag
# ---------------------------------------------
def projectile_odes(state, t):
    """
    state = [x, y, vx, vy]
    dx/dt = vx
    dy/dt = vy
    dvx/dt = -k * v * vx
    dvy/dt = -g - k * v * vy
    where v = sqrt(vx^2 + vy^2)
    """
    x, y, vx, vy = state
    v = math.sqrt(vx*vx + vy*vy)
    
    dxdt = vx
    dydt = vy
    dvxdt = -k * v * vx
    dvydt = -g - k * v * vy
    
    return [dxdt, dydt, dvxdt, dvydt]

# ---------------------------------------------
# 3) Helper function to get y at a specific x
# ---------------------------------------------
def get_y_at_x(x_target, angle_deg, velocity):
    """
    Numerically integrate until we reach x = x_target,
    then return the corresponding y value.
    
    angle_deg: launch angle in degrees
    velocity:  launch speed (m/s)
    """
    # Initial velocity components
    angle_rad = math.radians(angle_deg)
    vx0 = velocity * math.cos(angle_rad)
    vy0 = velocity * math.sin(angle_rad)
    
    # Initial state: x=0, y=0, vx=vx0, vy=vy0
    state0 = [0.0, 0.0, vx0, vy0]
    
    # Time array for integration (you may need to adjust the upper limit)
    t_span = np.linspace(0, 5, 501)  # 0 to 5 seconds, 501 steps
    
    # Integrate ODE
    sol = odeint(projectile_odes, state0, t_span)
    
    # The solution array 'sol' has shape (len(t_span), 4): columns are [x, y, vx, vy].
    # We look for the first time where x >= x_target.
    for i in range(len(t_span)):
        if sol[i, 0] >= x_target:
            return sol[i, 1]
    
    # If x_target not reached within t_span, return the last y or None
    return sol[-1, 1]

# ---------------------------------------------
# 4) Define the system of equations for fsolve
# ---------------------------------------------
def equations(p):
    """
    We want:
      y at x=wall_distance == wall_height
      y at x=goal_distance      == goes_in_height
    """
    angle_deg, velocity = p
    eq_wall = get_y_at_x(wall_distance, angle_deg, velocity) - wall_height
    eq_goal = get_y_at_x(goal_distance,      angle_deg, velocity) - goes_in_height
    return (eq_wall, eq_goal)

# -----------------------------



if __name__ == "__main__":
    # variables
    wall_distance = 9   
    wall_height = 2.4 
    goal_distance = 16 
    # constants
    goes_in_height= 2.25
    # 2.25 is the height for the bottom of the ball for the ball to go in
    # ~= 2.44 - 0.23 ----- goal height - ball size measured from the bottom! plus as much as it bounces in from the post
    g = 9.81                # gravitational acceleration (m/s^2)
    rho = 1.225             # air density (kg/m^3)
    r = 0.115                # approx. radius of soccer ball (m)
    A = math.pi * r * r     # cross-sectional area (m^2)
    m = 0.43                # mass of a typical soccer ball (kg)
    Cd = 0.25      # drag coefficient of a soccer ball (per NASA), May be changed according to field tests
    # Quadratic drag factor k = (1/2)*(rho)*(Cd)*(A) / m
    k = 0.5 * rho * Cd * A / m

    kick_angle_deg, launch_velocity_ms, max_kick_velocity_kmh, tangent_angle, horizontal_velocity, time_to_reach_goal = calculate_trajectory_params(goal_distance, wall_distance, wall_height)
    print(f"Kick angle: {kick_angle_deg:.2f}°")
    print(f"Velocity: {max_kick_velocity_kmh:.2f} km/h")
    plot_trajectory(kick_angle_deg, launch_velocity_ms, max_kick_velocity_kmh, tangent_angle, horizontal_velocity, time_to_reach_goal)
