import pygame
import math
from utilities import rotate_point

class UserInterface:
    def __init__(self, screen):
        self.screen = screen
        self.retro_font_path = "PressStart2P-Regular.ttf"
        self.retro_font = pygame.font.Font(self.retro_font_path, 32)

        # Dictionary to track previous UI positions
        # Format: {(alignment, level): (last_x, last_y, last_width, last_height)}
        self.ui_layout = {}


    def calculate_position(self, width, height, alignment, level, index, spacing=10):
        screen_width, screen_height = self.screen.get_size()

        # Determine vertical position
        if "top" in alignment:
            y = spacing + (height + spacing) * level  # Stacking downward
        elif "bottom" in alignment:
            y = screen_height - height - spacing - (height + spacing) * level  # Stacking upward
        else:  # "center" alignment
            y = (screen_height - height) // 2

        key = (alignment, level)  # Unique key to track stacking

        # Determine horizontal position
        if index == 0 or key not in self.ui_layout:
            # First item at this alignment & level
            if "right" in alignment:
                x = screen_width - width - spacing  # Start at right edge
            elif "left" in alignment:
                x = spacing  # Start at left edge
            else:  # "center" alignment
                x = (screen_width - width) // 2
        else:
            # Stack based on the previous item
            last_x, last_y, last_width, last_height = self.ui_layout[key]

            if "right" in alignment:
                x = last_x - (width + spacing)  # Stack to the left
            elif "left" in alignment:
                x = last_x + last_width + spacing  # Stack to the right
            else:
                x = (screen_width - width) // 2

        # Update stored position
        self.ui_layout[key] = (x, y, width, height)
        return x, y


    def draw_bar(self, capacity, max_capacity, bar_width, index, alignment):

        #if capacity < max_capacity:
        if True:
            bar_height = 20
            x, y = self.calculate_position(bar_width, bar_height, alignment=alignment, level=0, index=index)   
            fuel_ratio = capacity / max_capacity
            
            pygame.draw.rect(self.screen, (255, 255, 255), (x, y, bar_width * fuel_ratio, bar_height))
            pygame.draw.rect(self.screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)

 

    def draw_prompt(self, text, position, time):
        time_offset = time.time() * 3  # Adjust speed of wobble
        wobble = math.sin(time_offset) * 5  # Adjust amplitude of wobble
        font = pygame.font.Font(self.retro_font_path, 16)  # Default font, size 36
        
        text_surface = font.render(text, True, (255, 255, 255))  # White text
        position = position + + pygame.math.Vector2(wobble)
        self.screen.blit(text_surface, position)

    def show_message(self, text):
        # Fill the screen with black
        self.screen.fill((0, 0, 0))

        # Max width for wrapping
        max_width = self.screen.get_width() - 40  # Leave some margin on the sides
        lines = self.wrap_text(self.retro_font, text, max_width)

        # Calculate vertical position for centered text
        line_height = self.retro_font.get_linesize()
        total_height = len(lines) * line_height
        start_y = (self.screen.get_height() - total_height) // 2

        # Draw each line of text
        for i, line in enumerate(lines):
            text_surface = self.retro_font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, start_y + i * line_height))
            self.screen.blit(text_surface, text_rect)

        # Update the display
        pygame.display.flip()

        # Wait for user input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False  # Exit when any key is pressed

    def wrap_text(self, font, text, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            # Check if adding this word would exceed the max width
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] > max_width:
                # If it exceeds, finalize the current line and start a new one
                lines.append(current_line)
                current_line = word
            else:
                # Otherwise, add the word to the current line
                current_line = test_line

        # Add the last line
        if current_line:
            lines.append(current_line)

        return lines
    
    def draw_dotted_rect(self, surface, color, rect, dot_size=2, spacing=4):
        x, y, width, height = rect

        # Top edge
        for i in range(0, width, dot_size + spacing):
            pygame.draw.circle(surface, color, (x + i, y), dot_size)

        # Bottom edge
        for i in range(0, width, dot_size + spacing):
            pygame.draw.circle(surface, color, (x + i, y + height), dot_size)

        # Left edge
        for i in range(0, height, dot_size + spacing):
            pygame.draw.circle(surface, color, (x, y + i), dot_size)

        # Right edge
        for i in range(0, height, dot_size + spacing):
            pygame.draw.circle(surface, color, (x + width, y + i), dot_size)
    
    def draw_map(self, screen, player, spaceship, planets, map_width=200, map_height=200):
        """
        Draw a scrolling mini-map centered on the player.
        Only shows planets after they have been discovered.
        """
        # Create a mini-map surface
        map_surface = pygame.Surface((map_width, map_height))
        map_surface.fill((0, 0, 0))  # Black background
        pygame.draw.rect(map_surface, (255, 255, 255), (0, 0, map_width, map_height), 1)  # Border

        # Define the scale (reduce the game world size to fit the map)
        world_width, world_height = 6000, 6000  # Approximate game world size
        scale_x = map_width / world_width
        scale_y = map_height / world_height

        # Calculate offset so the player is at the center of the map
        player_map_x = player.position.x * scale_x
        player_map_y = player.position.y * scale_y
        map_offset_x = map_width // 2 - player_map_x
        map_offset_y = map_height // 2 - player_map_y

        def world_to_map(pos):
            """Convert world position to mini-map position with scrolling applied."""
            x = (pos.x * scale_x) + map_offset_x
            y = (pos.y * scale_y) + map_offset_y
            return int(x), int(y)

        # Draw only discovered planets
        for planet in planets:
            if not planet.discovered:
                continue  # Skip undiscovered planets

            planet_pos = world_to_map(planet.position)
            planet_radius = max(2, int(planet.radius * scale_x))  # Scale radius
            pygame.draw.circle(map_surface, (255, 255, 255), planet_pos, planet_radius, 1)  # White outline for planets

        # Draw the spaceship on the map
        spaceship_pos = world_to_map(spaceship.position)
        scale_factor = 0.5  # Scale down the spaceship for the mini-map
        triangle_points = [
            (0, -10 * scale_factor),  # Nose (front of triangle)
            (-5 * scale_factor, 5 * scale_factor),  # Bottom-left
            (5 * scale_factor, 5 * scale_factor)    # Bottom-right
        ]

        # Rotate the triangle 90 degrees clockwise by adding 90 degrees to the spaceship angle
        rotated_points = [
            rotate_point(0, 0, math.radians(spaceship.angle + 90), px, py)
            for px, py in triangle_points
        ]

        transformed_points = [
            (spaceship_pos[0] + int(px), spaceship_pos[1] + int(py))
            for px, py in rotated_points
        ]

        pygame.draw.polygon(map_surface, (255, 255, 255), transformed_points, 1)  # White outline for spaceship

        # Draw the player on the map (always centered)
        pygame.draw.circle(map_surface, (255, 255, 255), (map_width // 2, map_height // 2), 2)  # White dot for player

        # Determine UI placement
        x, y = self.calculate_position(map_width, map_height, ("right", "top"), 0, 0)

        # Blit the map onto the main screen
        screen.blit(map_surface, (x, y))  # Top-right corner



    def draw_planet_indicators(self, screen, camera, planet):
        screen_width, screen_height = screen.get_size()
        margin = 20  # Distance from the screen edge
        arrow_size = 15  # Size of the arrow
        arrow_thickness = 2  # Thickness of the arrow lines
        
        # Convert planet world position to screen coordinates
        planet_screen_pos = camera.apply(planet)
        px, py = int(planet_screen_pos.x), int(planet_screen_pos.y)
        pr = camera.get_zoomed_value(planet.radius + 100)  # Scale the planet radius with camera zoom

        # Check if any part of the planet is still visible
        if (
            (px + pr) >= 0 and (px - pr) <= screen_width and
            (py + pr) >= 0 and (py - pr) <= screen_height
        ):
            return

        # Determine which edge of the screen to place the indicator
        if px + pr < 0:  # Left edge
            arrow_x, arrow_y = margin, min(max(py, margin), screen_height - margin)
            direction = "left"
        elif px - pr > screen_width:  # Right edge
            arrow_x, arrow_y = screen_width - margin, min(max(py, margin), screen_height - margin)
            direction = "right"
        elif py + pr < 0:  # Top edge
            arrow_x, arrow_y = min(max(px, margin), screen_width - margin), margin
            direction = "up"
        else:  # Bottom edge
            arrow_x, arrow_y = min(max(px, margin), screen_width - margin), screen_height - margin
            direction = "down"

        # Draw the directional arrow
        self.draw_arrow(screen, arrow_x, arrow_y, direction, arrow_size, arrow_thickness)


    def draw_arrow(self, screen, x, y, direction, size=10, thickness=2):
        color = (255, 255, 255)  # White arrow

        if direction == "left":
            points = [(x + size, y - size), (x, y), (x + size, y + size)]
        elif direction == "right":
            points = [(x - size, y - size), (x, y), (x - size, y + size)]
        elif direction == "up":
            points = [(x - size, y + size), (x, y), (x + size, y + size)]
        else:  # "down"
            points = [(x - size, y - size), (x, y), (x + size, y - size)]

        pygame.draw.lines(screen, color, False, points, thickness)

    def draw_discovery_message(self, screen, message):
        font = pygame.font.Font(self.retro_font_path, 24)
        text_surface = font.render(message, True, (255, 255, 255))
        
        # Position at the top-center of the screen
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text_surface, text_rect)

    def display_debug(self, screen, spaceship, planets, player):
        font = pygame.font.Font(self.retro_font_path, 16)

        debug_info = [
            f"Player: Pos ({round(player.position.x)}, {round(player.position.y)}), "
            f"Vel ({round(player.velocity.x)}, {round(player.velocity.y)}), Boost {round(player.fuel)}/{round(player.max_fuel)}",

            f"Spaceship: Pos ({round(spaceship.position.x)}, {round(spaceship.position.y)}), "
            f"Vel ({round(spaceship.velocity.x)}, {round(spaceship.velocity.y)}), "
            f"Fuel {round(spaceship.fuel_amount)}/{round(spaceship.max_fuel)}, "
            f"boost {round(spaceship.boost_cylinder_amount)}/{round(spaceship.boost_cylinder_capacity)}"
        ]

        # Add planet info
        for i, planet in enumerate(planets):
            debug_info.append(
                f"Planet {i}: Pos ({round(planet.position.x)}, {round(planet.position.y)}), "
                f"Mass {round(planet.mass)}, Radius {round(planet.radius)}, "
                f"Discovered: {planet.discovered}"
            )

        # Render and display all debug info line by line
        for idx, line in enumerate(debug_info):
            text_surface = font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(topleft=(10, screen.get_height() // 2 + idx * 20))
            screen.blit(text_surface, text_rect)
