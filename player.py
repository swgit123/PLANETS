import pygame
from physics_object import PhysicsObject
from utilities import calculate_gravitational_force, get_tangential_vector
import random
import math 
from particle import Particle

class Player(PhysicsObject):
    def __init__(self, x, y, mass, radius):
        super().__init__(x, y, mass, radius)
        self.on_ground = True
        self.in_space = False
        self.in_ship = False  # Track if the player is inside the spaceship
        self.fuel = 30  # Initialize fuel level
        self.max_fuel = 30  # Maximum fuel capacity
        self.fuel_regen_rate = 15  # Fuel regeneration rate per second
        self.jump_fuel_cost = 1  # Fuel cost per jump or use
        self.key_cooldown = 0
        self.trail = []  # Store recent positions for the trail
        self.trail_max_length = 20  # Maximum number of trail points
        self.dt = None
        

    def regenerate_fuel(self, dt):
        if self.on_ground:
            self.fuel = min(self.max_fuel, self.fuel + self.fuel_regen_rate * dt)

    def update(self, dt, planets, spaceship):
        self.dt = dt  # Store delta time for scaling forces
        if not self.in_ship:  # Only update if the player is not inside the spaceship
            if not self.on_ground:
                self.apply_gravity(planets)
            super().update(dt)
            self.check_collision_with_planets(planets)
            self.regenerate_fuel(dt)
            self.update_trail()  # Update the trail when the player moves


    def update_trail(self):
        """Update the trail with the player's current position."""
        self.trail.append((self.position.x, self.position.y))
        if len(self.trail) > self.trail_max_length:
            self.trail.pop(0)  # Remove the oldest point if the trail exceeds max length

    def check_collision_with_planets(self, planets):
        self.on_ground = False  # Assume not on ground unless collision detected
        self.in_space = True    # Assume in space unless near a planet
        for planet in planets:
            collision_vector = planet.position - self.position
            distance = collision_vector.length()
            collision_distance = planet.radius + self.radius

            if distance < collision_distance:
                self.on_ground = True
                self.in_space = False

                # Calculate overlap and adjust position
                overlap = collision_distance - distance
                if distance > 0:  # Avoid division by zero
                    collision_normal = collision_vector.normalize()
                    self.position -= collision_normal * overlap  # Push out of collision

                    # Collision response: Zero out velocity in the collision normal direction
                    velocity_normal_component = self.velocity.dot(collision_normal) * collision_normal
                    self.velocity -= velocity_normal_component

                break  # Exit after handling collision
            else:
                # Check for proximity to manage in_space status
                if distance - planet.radius < 100:
                    self.in_space = False  # Player is near a planet

        if self.on_ground:
            self.in_space = False

    def draw(self, screen, camera):
        # Draw the trail
        
        # Draw the current player position
        draw_pos = camera.apply(self)
        radius = camera.get_zoomed_value(self.radius)
        pygame.draw.circle(screen, (255, 255, 255), (int(draw_pos.x), int(draw_pos.y)), radius, 3)


    def handle_movement(self, planet, keys, spaceship, dt):
        speed = 50  # Base walking speed
        jump_speed = 300  # Base jump speed

        self.dt = dt
        tangential_vector = get_tangential_vector(self.position, planet.position)
        radial_vector = self.position - planet.position
        normal_vector = radial_vector.normalize()  # This points directly away from the planet

        if keys[pygame.K_a]:
            # Move left along the tangent
            self.apply_force(tangential_vector * -speed)  # Scale force by dt
        if keys[pygame.K_d]:
            # Move right along the tangent
            self.apply_force(tangential_vector * speed)  # Scale force by dt
        if keys[pygame.K_s]:
            # Move down towards the planet
            self.apply_force(normal_vector * -jump_speed * 2)

        # Jump logic with fuel consumption
        if keys[pygame.K_w] and self.fuel >= self.jump_fuel_cost:
            # Only jump if fuel is available
            self.apply_force(normal_vector * jump_speed)  # Scale jump force by dt
            self.fuel -= self.jump_fuel_cost  # Decrease fuel
            self.on_ground = False  # Ensure the player can't jump again until they land

        self.velocity *= 0.98  # Damping factor for velocity
