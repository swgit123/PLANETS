from particle import Particle
import pygame
from physics_object import PhysicsObject
import math
import random
from utilities import rotate_point
from user_interface import UserInterface

class Spaceship(PhysicsObject):
    def __init__(self, planet, x, y, mass, radius):
        super().__init__(x, y, mass, radius)
        self.planet = planet
        self.angle = 0  # Angle of rotation in degrees
        self.rotation_speed = 150
        self.boost_force = 25000
        self.reverse_boost_force = 25000
        self.particles = []  # List to store particles

        #Fuel system
        self.fuel_amount = 50
        self.max_fuel = 1000
        self.boost_cylinder_capacity = 150  # Maximum fuel capacity
        self.boost_cylinder_amount = 0
        self.boost_regen_rate = 40  # Fuel regeneration rate per second
        self.boost_cost = 1  # Fuel cost per jump or use
        self.boost_cost_per_second = 60

        #oxygen system
        self.max_oxygen = 50  # Maximum oxygen capacity
        self.oxygen_amount = self.max_oxygen  # Current oxygen level
        self.oxygen_depletion_rate = 5  # Oxygen loss per second
        self.oxygen_regen_rate = 10  # Oxygen gained per second inside atmosphere


    def regenerate_oxygen(self, dt):
        self.oxygen_amount = min(self.max_oxygen, self.oxygen_amount + self.oxygen_regen_rate * dt)

    def deplete_oxygen(self, dt):
        self.oxygen_amount = max(0, self.oxygen_amount - self.oxygen_depletion_rate * dt)


    def regenerate_boost(self, dt):
        # Calculate the amount to transfer from fuel to boost cylinder
        regen_amount = self.boost_regen_rate * dt

        # Ensure we don't exceed the boost cylinder's capacity or deplete the fuel below zero
        actual_regen = min(regen_amount, self.boost_cylinder_capacity - self.boost_cylinder_amount, self.fuel_amount)

        # Update the boost cylinder and reduce fuel accordingly
        self.boost_cylinder_amount += actual_regen
        self.fuel_amount -= actual_regen


    def handle_movement(self, keys, dt):

        #rocket_thrust = pygame.mixer.Sound("assets/rocket_thrust.ogg")
        """Handle input for spaceship movement."""
        if keys[pygame.K_w]:
            # Apply thrust in the forward direction
            thrust = pygame.math.Vector2(
                self.boost_force * math.cos(math.radians(self.angle)),
                self.boost_force * math.sin(math.radians(self.angle))
            )
            boost_cost = self.boost_cost_per_second * dt
            if self.boost_cylinder_amount >= boost_cost:
                self.boost_cylinder_amount -= boost_cost
                self.apply_force(thrust)
                self.create_particles(forward=True)
                #rocket_thrust.play()

        if keys[pygame.K_s]:
            # Apply reverse thrust
            reverse_thrust = pygame.math.Vector2(
                self.reverse_boost_force * math.cos(math.radians(self.angle + 180)),
                self.reverse_boost_force * math.sin(math.radians(self.angle + 180))
            )
            boost_cost = self.boost_cost_per_second * dt

            if self.boost_cylinder_amount >= boost_cost:
                self.boost_cylinder_amount -= boost_cost
                self.apply_force(reverse_thrust)
                self.create_particles(forward=False)

        if not keys[pygame.K_s] and not keys[pygame.K_w]:
            #rocket_thrust.stop()
            self.regenerate_boost(dt)

        

        # Rotate the spaceship
        rotation_amount = self.rotation_speed * dt
        if keys[pygame.K_a]:
            self.angle -= rotation_amount
        if keys[pygame.K_d]:
            self.angle += rotation_amount


    def create_particles(self, forward):
        """Create particles for visual feedback when thrusting."""
        # The direction to spawn particles (reverse for forward thrust, forward for reverse thrust)
        spawn_angle = math.radians(self.angle + (180 if forward else 0))  # Adjust particle spawn direction
        rear_offset_distance = 15  # Distance from the center to the back of the ship

        # Calculate the rear position of the spaceship
        rear_x = self.position.x - math.cos(math.radians(self.angle)) * rear_offset_distance
        rear_y = self.position.y - math.sin(math.radians(self.angle)) * rear_offset_distance

        for _ in range(5):  # Create multiple particles
            particle_angle = spawn_angle + random.uniform(-0.2, 0.2)  # Slight random spread in particle direction
            particle_speed = random.uniform(1, 3)  # Random speed for particles
            particle = Particle(
                x=rear_x,
                y=rear_y,
                angle=particle_angle,  # Direction the particle will travel
                speed=particle_speed,  # Speed of the particle
                lifetime=random.randint(10, 20)  # Random lifetime
            )
            self.particles.append(particle)




    def update_particles(self, dt, planets):
        """Update the particles and remove expired ones."""
        for particle in self.particles:
            particle.update(dt)
        self.particles = [p for p in self.particles if p.lifetime > 0]  # Keep only active particles

    def check_collision_with_planets(self, planets):
        """Check and handle collisions with planets."""
        for planet in planets:
            collision_vector = planet.position - self.position
            distance = collision_vector.length()
            collision_distance = planet.radius + self.radius

            if distance < collision_distance:
                # Collision detected: Push the ship out of the collision
                overlap = collision_distance - distance
                collision_normal = collision_vector.normalize()
                self.position -= collision_normal * overlap

                # Apply a bounce effect by inverting and reducing the velocity in the collision normal direction
                velocity_normal_component = self.velocity.dot(collision_normal) * collision_normal
                self.velocity *= -0.5  # Reverse and damp velocity
                break  # Handle one collision at a time

    

    def update(self, dt, keys, planets, player):
        """Update spaceship physics and handle input."""
        self.apply_gravity(planets)  # Always apply gravity to the spaceship
        self.check_collision_with_planets(planets)  # Always check for collisions

        #self.regenerate_fuel(dt)  # Regenerate fuel over time
        self.update_particles(dt=dt, planets=planets)  # Update particles

        in_atmosphere = any((self.position - planet.position).length() <= (planet.radius + 100) for planet in planets)
    
        if in_atmosphere:
            self.regenerate_oxygen(dt)
        else:
            self.deplete_oxygen(dt)
       
        super().update(dt)  # Update position and velocity


    def draw(self, screen, camera):
        """Draw a classic spaceship resembling the one from Asteroids."""
        # Define the points of the spaceship relative to its center
        points = [
            (10, 0),    # Nose (front)
            (-5, -5),   # Left tail
            (-3, 0),    # Bottom center
            (-5, 5)     # Right tail
        ]

        # Rotate points based on the spaceship's angle (adjusted for orientation)
        rotated_points = [
            rotate_point(0, 0, math.radians(self.angle), px, py)
            for px, py in points
        ]

        # Apply camera transformation to the spaceship's position
        base_draw_position = camera.apply(self)
        transformed_points = [
            (base_draw_position.x + px * camera.zoom, base_draw_position.y + py * camera.zoom)
            for px, py in rotated_points
        ]

        # Convert the transformed points to integers for drawing
        transformed_points = [(int(p[0]), int(p[1])) for p in transformed_points]

        # Draw the spaceship
        pygame.draw.polygon(screen, (255, 255, 255), transformed_points, 3)

        # Draw particles
        for particle in self.particles:
            particle.draw(screen, camera)

