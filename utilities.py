import math
import pygame 

def calculate_gravitational_force(obj1, obj2, G=200):
    """Calculate and apply gravitational force from obj2 to obj1."""
    direction = obj2.position - obj1.position
    distance = direction.length()
    if distance > 0:
        direction = direction.normalize()
        force_magnitude = G * obj1.mass * obj2.mass / (distance ** 2)
        obj1.apply_force(direction * force_magnitude)

def circumference(radius):
    """Calculate the circumference of a circle."""
    return 2 * math.pi * radius

def position_on_orbit(center_x, center_y, radius, linear_position):
    """Calculate position along an orbit given a linear distance."""
    angle = (linear_position / circumference(radius)) * 360  # Convert linear position to angle in degrees
    angle_rad = math.radians(angle)  # Convert angle in degrees to radians
    x = center_x + radius * math.cos(angle_rad)
    y = center_y + radius * math.sin(angle_rad)
    return (x, y)

def rotate_point(cx, cy, angle, px, py):
    """Rotate a point (px, py) around a center (cx, cy) by an angle in radians."""
    s, c = math.sin(angle), math.cos(angle)
    px, py = px - cx, py - cy
    x_new = px * c - py * s + cx
    y_new = px * s + py * c + cy
    return x_new, y_new

def get_tangential_vector(player_position, planet_position):
    # Calculate radial vector
    radial_vector = player_position - planet_position
    # Rotate radial vector by 90 degrees to get tangential vector
    tangential_vector = pygame.math.Vector2(-radial_vector.y, radial_vector.x)
    return tangential_vector.normalize()
