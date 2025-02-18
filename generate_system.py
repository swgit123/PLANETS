import random
import math
import matplotlib.pyplot as plt
import random
from planet import Planet
import pygame


def generate_planets(planet_amount = 10, distance=1500):

    distance = 1500  # Distance between planets
    
    positions = [(0, 0)]  # Start at (0,0)
    angle = random.uniform(0, 360)  # Initial random angle

    planets = []
    
    for i in range(planet_amount):
        # Get the last position
        x, y = positions[-1]
        
        # Calculate new position
        new_x = x + distance * math.cos(math.radians(angle))
        new_y = y + distance * math.sin(math.radians(angle))
        positions.append((new_x, new_y))
        
        # Adjust the angle randomly between -90 and +90 degrees
        angle += random.uniform(-90, 90)

        radius = 200
        mass = 50000

        color = (
                random.randint(100, 255), 
                random.randint(100, 255), 
                random.randint(100, 255)
            )
        
        planets.append(Planet(x, y, mass, radius, color))

        
    
    return planets





# # Generate positions
# positions = generate_positions()

# def generate_planets(num_planets, world_size, min_distance=700, min_radius=100, max_radius=300):

#     planets = []
#     max_attempts = 1000  # To prevent infinite loops

#     for _ in range(num_planets):
#         attempts = 0
#         while attempts < max_attempts:
#             # Random position in the world bounds
#             x = random.randint(min_radius, world_size[0] - min_radius)
#             y = random.randint(min_radius, world_size[1] - min_radius)

#             # Random size and mass
#             #radius = random.randint(min_radius, max_radius)
#             #mass = radius * 250  # Mass scales with size
#             radius = 200
#             mass = 50000

#             # Random color (grayscale or slight color variations)
#             color = (
#                 random.randint(100, 255), 
#                 random.randint(100, 255), 
#                 random.randint(100, 255)
#             )

#             # Ensure it doesn’t overlap with existing planets
#             too_close = any((pygame.math.Vector2(x, y) - p.position).length() < (p.radius + radius + min_distance) for p in planets)

#             if not too_close:
#                 planets.append(Planet(x, y, mass, radius, color))
#                 break  # Move to the next planet

#             attempts += 1

#     return planets



# def visualation(): 
#     # Extract x and y coordinates
#     x_vals, y_vals = zip(*positions)

#     # Plot the points
#     plt.figure(figsize=(8, 8))
#     plt.plot(x_vals, y_vals, marker='o', linestyle='-', markersize=8, label="Path")

#     # Highlight the start and end points
#     plt.scatter(x_vals[0], y_vals[0], color='green', s=100, label="Start")
#     plt.scatter(x_vals[-1], y_vals[-1], color='red', s=100, label="End")

#     # Annotate points
#     for i, (x, y) in enumerate(positions):
#         plt.text(x, y, f"{i}", fontsize=12, ha='right')

#     plt.xlabel("X Position")
#     plt.ylabel("Y Position")
#     plt.title("System Map")
#     plt.legend()
#     plt.grid(True)
#     plt.axis("equal")
#     plt.show()
