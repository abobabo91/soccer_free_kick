from scipy.optimize import fsolve
import math
import numpy as np
import matplotlib.pyplot as plt


def calculate_trajectory_params(distance, wall_distance, wall_height):
    # Constants
    goes_in_height = 2.25
    ball_diameter = 0.23
    goal_height = 2.44
    # 2.25 is the height for the bottom of the ball for the ball to go in
    # ~= 2.44 - 0.23 ----- goal height - ball size measured from the bottom! plus as much as it bounces in from the post

    def equations(p, distance=distance, wall_height=wall_height, wall_distance=wall_distance):
        tangent_angle, horizontal_velocity = p
        return (
            wall_distance * tangent_angle - (9.81 / 2) * wall_distance**2 / horizontal_velocity**2 - wall_height, 
            distance * tangent_angle - (9.81 / 2) * distance**2 / horizontal_velocity**2 - goes_in_height
        )
    
    tangent_angle, horizontal_velocity = fsolve(equations, (1, 1))
    
    kick_angle = math.degrees(math.atan(tangent_angle))
    max_kick_velocity = horizontal_velocity / math.cos(math.atan(tangent_angle))
    max_kick_velocity_kmh = max_kick_velocity * 3.6
    
    time_to_reach_goal = distance / horizontal_velocity
    
    return kick_angle, max_kick_velocity, tangent_angle, horizontal_velocity, time_to_reach_goal






#-------------------visualization

def plot_trajectory(kick_angle, max_kick_velocity, tangent_angle, horizontal_velocity, time_to_reach_goal):
    time_steps = np.linspace(0, time_to_reach_goal, 100)
    horizontal_positions = horizontal_velocity * time_steps
    vertical_positions = tangent_angle * horizontal_positions - (9.81 / 2) * (horizontal_positions / horizontal_velocity)**2
    
    plt.figure(figsize=(10, 5))
    plt.plot(horizontal_positions, vertical_positions, label="Ball trajectory", color="blue")
    
    # Draw ball trajectory width
    plt.plot(horizontal_positions, vertical_positions + ball_diameter, color="blue")
    
    # Draw wall
    plt.plot([wall_distance, wall_distance], [0, wall_height], color="red", linewidth=2, label="Wall")
    
    # Draw goal
    plt.plot([distance, distance], [0, goal_height], color="green", linewidth=2, label="Goal")
    
    # Formatting the plot
    plt.title("Ball Trajectory Visualization")
    plt.xlabel("Horizontal Distance (m)")
    plt.ylabel("Height (m)")
    plt.axhline(0, color="black", linewidth=0.5)  # Ground line
    plt.xlim(0, distance + 2)  # Slightly extend beyond the goal
    plt.ylim(0, max(goal_height, max(vertical_positions)) + 1)  # Allow for some headroom
    plt.legend()
    plt.grid()
    
    plt.annotate(
        f"Angle: {kick_angle:.2f}°",
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
        f"Goal distance: {distance:.2f}m",
        fontsize=10,
        color="red"
    )
    
    plt.show()



if __name__ == "__main__":
    # Variables
    distance = 25
    wall_height = 2.5
    wall_distance = 9

    kick_angle, max_kick_velocity, tangent_angle, horizontal_velocity, time_to_reach_goal = calculate_trajectory_params(distance, wall_distance, wall_height)
    print(f"Kick angle: {kick_angle:.2f}°")
    print(f"Velocity: {max_kick_velocity * 3.6:.2f} km/h")
    plot_trajectory(kick_angle, max_kick_velocity, tangent_angle, horizontal_velocity, time_to_reach_goal)

