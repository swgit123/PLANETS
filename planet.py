
import pygame
from physics_object import PhysicsObject
import math 
import random
from utilities import position_on_orbit
from fuel_tanks import FuelTank
import noise

def draw_dotted_circle(surface, color, draw_pos, radius, dot_radius=2, num_dots=50):
    cx, cy = draw_pos
    for i in range(num_dots):
        # Calculate the angle for each dot
        angle = (2 * math.pi / num_dots) * i
        # Calculate the dot's position
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        # Draw the dot
        pygame.draw.circle(surface, color, (int(x), int(y)), dot_radius)



class Planet(PhysicsObject):
    def __init__(self, x, y, mass, radius, color):
        super().__init__(x, y, mass, radius)
        self.color = color
       
        #self.num_trees = random.randint(5, 15)  # Random number of trees
        self.num_trees = random.randint(25, 40)
        self.trees = self.generate_trees()

        self.num_fuel_tanks = random.randint(3, 7)  # Random number of fuel tanks
        self.fuel_tanks = self.generate_fuel_tanks()

        self.discovered = False 

        

    def generate_trees(self):
        trees = []
        for _ in range(self.num_trees):
            angle = random.uniform(0, 2 * math.pi)
            height = random.randint(18, 23)  # Height of the tree
            branch_length = random.randint(5, 15) * height * (12/20) # Length of branches
            levels = random.randint(3, 6)  # Number of branch levels
            x_offset = self.radius * math.cos(angle)
            y_offset = self.radius * math.sin(angle)
            trees.append((x_offset, y_offset, height, branch_length, levels))
        return trees
    
    def generate_fuel_tanks(self):
        """
        Generate fuel tanks randomly around the planet's orbit.
        """
        fuel_tanks = []
        for _ in range(self.num_fuel_tanks):
            linear_position = random.uniform(0, self.radius * 2 * math.pi)  # Random position along the orbit
            x, y = position_on_orbit(self.position.x, self.position.y, self.radius + 1, linear_position)  # Slightly outside the planet
            fuel_tanks.append(FuelTank(x, y))
        return fuel_tanks


    def draw_tree(self, screen, camera, base_x, base_y, angle, zoom, tree):
        trunk_height = 20 * zoom  # Scale trunk height with zoom
        branch_base_length = 12 * zoom  # Base branch length
        base = pygame.math.Vector2(base_x, base_y)

        # Trunk endpoint (pointing outward from the planet center)
        trunk_end = base + pygame.math.Vector2(trunk_height * math.cos(angle), trunk_height * math.sin(angle))

        # Draw the trunk
        pygame.draw.line(screen, (255, 255, 255), (base.x, base.y), (trunk_end.x, trunk_end.y), 3)

        # Draw branches
        num_branch_levels = 6  # Increase for more density
        branch_angle_offset = math.pi / 4  # Downward tilt of branches
        for i in range(num_branch_levels):
            # Reverse branch ratio to make smaller branches at the top
            branch_ratio = (num_branch_levels - 1 - i) / (num_branch_levels - 1) * 0.5  # Top 50%
            branch_base = base + pygame.math.Vector2(
                (1 - branch_ratio) * trunk_height * math.cos(angle),
                (1 - branch_ratio) * trunk_height * math.sin(angle)
            )

            # Adjust branch length for levels (smaller at top)
            branch_length = branch_base_length * branch_ratio

            # Left branch (angled downward relative to trunk)
            left_branch_angle = angle + math.pi + branch_angle_offset  # Adjusted to tilt downward
            left_branch_end = branch_base + pygame.math.Vector2(
                branch_length * math.cos(left_branch_angle),
                branch_length * math.sin(left_branch_angle)
            )
            pygame.draw.line(screen, (255, 255, 255), (branch_base.x, branch_base.y), (left_branch_end.x, left_branch_end.y), 3)

            # Right branch (angled downward relative to trunk)
            right_branch_angle = angle + math.pi - branch_angle_offset  # Adjusted to tilt downward
            right_branch_end = branch_base + pygame.math.Vector2(
                branch_length * math.cos(right_branch_angle),
                branch_length * math.sin(right_branch_angle)
            )
            pygame.draw.line(screen, (255, 255, 255), (branch_base.x, branch_base.y), (right_branch_end.x, right_branch_end.y), 3)

    def draw(self, screen, transparent_surface, camera, time, player_position):
        draw_pos = camera.apply(self)
        radius = camera.get_zoomed_value(self.radius)
        
        # Draw the planet
        pygame.draw.circle(screen, (255, 255, 255), (int(draw_pos.x), int(draw_pos.y)), radius, 3)
           
        # Calculate distance between the player and the planet's center
        distance_to_player = (self.position - player_position).length()
        # Check if the player is inside the atmosphere
        if distance_to_player <= (self.radius + 100) or True:

            # atmosphere_radius = radius + camera.get_zoomed_value(100)

            # # Draw atmosphere with a fading dark edge
            # base_color = (135, 206, 250)  # Sky blue base
            # for i in range(1, 15):  # More steps = smoother transition
            #     fade_factor = i / 15  # Increases from 0 to 1
            #     darkened_color = (
            #         int(base_color[0] * (1 - fade_factor * 0.6)),  # Reduce brightness towards edge
            #         int(base_color[1] * (1 - fade_factor * 0.6)),
            #         int(base_color[2] * (1 - fade_factor * 0.6)),
            #         80  # Constant alpha to keep visibility
            #     )
            #     pygame.draw.circle(
            #         transparent_surface,
            #         darkened_color,
            #         (int(draw_pos.x), int(draw_pos.y)),
            #         int(atmosphere_radius * (1 - fade_factor * 0.05))
            #     )

            pygame.draw.circle(
                transparent_surface,
                (135, 206, 250, 25),
                (int(draw_pos.x), int(draw_pos.y)),
                radius + camera.get_zoomed_value(100)
            )

            # Draw trees
            for tree in self.trees:
                # Calculate tree base position
                tree_x = draw_pos.x + camera.get_zoomed_value(tree[0])
                tree_y = draw_pos.y + camera.get_zoomed_value(tree[1])
                # Use the angle to make the tree point outward
                tree_angle = math.atan2(tree[1], tree[0])  # Calculate the outward angle
                self.draw_tree(screen, camera, tree_x, tree_y, tree_angle, camera.zoom, tree)

            # Draw fuel tanks
            for tank in self.fuel_tanks:
                tank.draw(screen, camera)
        else: 
            # Draw dotted circle for atmosphere
            draw_dotted_circle(screen, (255, 255, 255), (int(draw_pos.x), int(draw_pos.y)), radius + camera.get_zoomed_value(100), dot_radius=1, num_dots=150)
