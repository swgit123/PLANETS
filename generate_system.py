import random
import math
import matplotlib.pyplot as plt
import random
from planet import Planet
import pygame
import matplotlib.pyplot as plt


def generate_positions(planet_amount = 10, distance=1500):

    distance = 1500  # Distance between planets
    
    positions = [(0, 0)]  # Start at (0,0)
    angle = random.uniform(0, 360)  # Initial random angle

    
    
    for i in range(planet_amount):
        # Get the last position
        x, y = positions[-1]
        
        # Calculate new position
        new_x = x + distance * math.cos(math.radians(angle))
        new_y = y + distance * math.sin(math.radians(angle))
        positions.append((new_x, new_y))
        
        # Adjust the angle randomly between -90 and +90 degrees
        angle += random.uniform(-90, 90)
    
    
    return positions



def generate_planets(planet_amount = 10, distance=1500):
    positions = generate_positions(planet_amount = 10, distance=1500)
    #visualization(positions)
    planets = []
    for i, (x, y) in enumerate(positions):
        radius = 200
        mass = 50000

        color = (
                random.randint(100, 255), 
                random.randint(100, 255), 
                random.randint(100, 255)
            )
        
        planets.append(Planet(x, y, mass, radius, color))
    return planets



def visualization(positions): 
    #positions = generate_positions(planet_amount = 10, distance=1500)
    # Extract x and y coordinates
    x_vals, y_vals = zip(*positions)

    # Plot the points
    plt.figure(figsize=(8, 8))
    plt.plot(x_vals, y_vals, marker='o', linestyle='-', markersize=8, label="Path")

    # Highlight the start and end points
    plt.scatter(x_vals[0], y_vals[0], color='green', s=100, label="Start")
    plt.scatter(x_vals[-1], y_vals[-1], color='red', s=100, label="End")

    # Annotate points
    for i, (x, y) in enumerate(positions):
        plt.text(x, y, f"{i}", fontsize=12, ha='right')

    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.title("System Map")
    plt.legend()
    plt.grid(True)
    plt.axis("equal")
    plt.show()

# positions = generate_positions(planet_amount = 10, distance=1500)
# visualization(positions)



