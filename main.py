import pygame
from physics_object import PhysicsObject
from planet import Planet
from utilities import calculate_gravitational_force
from camera import Camera
from player import Player
from spaceship import Spaceship
from user_interface import UserInterface
import sys
import time
from procedural_generation import generate_planets
import time
import math


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#WIDTH, HEIGHT = 1200, 900
WIDTH, HEIGHT = 1920, 1080

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("P L A N E T S")

# Fonts
pygame.font.init()
retro_font_path = "PressStart2P-Regular.ttf"  # Adjust this path to your font file
title_font = pygame.font.Font(retro_font_path, 40)  # Adjust size for title
small_font = pygame.font.Font(retro_font_path, 20)  # Adjust size for instructions

def handle_keys(player, planet, keys, spaceship, ui, camera, dt):
    if player.key_cooldown > 0:
        player.key_cooldown -= 1  # Reduce cooldown timer

    if player.in_ship:
        prompt_position = camera.apply(spaceship) + pygame.math.Vector2(20, 20)

        
        if spaceship.fuel_amount <= 1 and spaceship.boost_cylinder_amount <= 1:
            prompt_position = camera.apply(spaceship) + pygame.math.Vector2(20, 20)
            ui.draw_prompt("Fuel empty", prompt_position, time)

        player.position = spaceship.position
        spaceship.handle_movement(keys, dt)
        if keys[pygame.K_e] and player.key_cooldown == 0:
            # Exit the spaceship
            spaceship.in_ship = False
            player.in_ship = False
            player.key_cooldown = 15  # Set a cooldown of 15 frames (adjust as needed)

            # Place the player slightly outside the spaceship
            exit_offset = pygame.math.Vector2(20, 0)  # Adjust the offset as needed
            exit_offset.rotate_ip(spaceship.angle)  # Rotate based on spaceship's angle
            player.position = spaceship.position + exit_offset

        

            

        
     
    else:
        if (spaceship.position - player.position).length() < 25 and not player.in_ship:         
            prompt_position = camera.apply(spaceship) + pygame.math.Vector2(20, 20)
            ui.draw_prompt("E to pilot", prompt_position, time)
            
            if keys[pygame.K_e] and player.key_cooldown == 0:
                
                # Enter the spaceship
                spaceship.in_ship = True
                player.in_ship = True
                player.key_cooldown = 15  # Set a cooldown of 15 frames
                
        player.handle_movement(planet, keys, spaceship, dt)


def adjust_zoom_based_on_distance(camera, distance, player):
    # Define a breakpoint distance and corresponding fixed zoom level
    breakpoint_distance = 100  # Distance threshold

    if not player.in_ship:
        fixed_zoom_level = 10  # Fixed zoom level for distances below the threshold
    else:
        fixed_zoom_level = 5

    # Parameters for zoom adjustment based on distance
    min_zoom = 1  # Minimum zoom when far from any planet
    max_zoom = 5  # Maximum zoom when above the breakpoint but very close to a planet
    zoom_sensitivity = 6  # Sensitivity of zoom changes based on distance

    # Smooth zoom calculation
    if distance < breakpoint_distance:
        target_zoom = fixed_zoom_level
    else:
        # Calculate zoom based on distance using an inverse relationship
        distance_factor = max(0, distance - breakpoint_distance)
        zoom = max_zoom - (distance_factor / zoom_sensitivity)
        zoom = max(min_zoom, min(zoom, max_zoom))
        target_zoom = zoom

    # Exponential smoothing for zoom transition
    smoothing_factor = 0.05  # Adjust this for a smoother or more responsive change
    camera.zoom += (target_zoom - camera.zoom) * smoothing_factor


def distance_to_nearest_planet(entity, planets):
    min_distance = float('inf')
    closest_planet = None
    for planet in planets:
        distance = (planet.position - entity.position).length() - planet.radius
        if distance < min_distance:
            min_distance = distance
            closest_planet = planet

    return min_distance, closest_planet


def spawn_on_planet(planet, angle_degrees, offset=0):
    angle_radians = math.radians(angle_degrees)
    x = planet.position.x + (planet.radius + offset) * math.cos(angle_radians)
    y = planet.position.y + (planet.radius + offset) * math.sin(angle_radians)
    return x, y


def draw_title_screen():
    screen.fill(BLACK)

    # Title text
    title_text = title_font.render("PLANETS", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(title_text, title_rect)

    # Instructions
    instruction_text = small_font.render("Press SPACE to Start", True, WHITE)
    instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(instruction_text, instruction_rect)

    # Optional retro-style border or effects
    pygame.draw.rect(screen, WHITE, (50, 50, WIDTH - 100, HEIGHT - 100), 1)

def title_screen_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False  # Exit the title screen loop when Enter is pressed

        draw_title_screen()
        pygame.display.flip()
        #


def main():
    screen_width = 1200
    screen_height = 900
    window_size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(window_size)
    ui = UserInterface(screen)  
    
    title_screen_loop()
    
    ui.show_message("You awake on a barren planet... Seemingly alone... How did you get here...?")
     
    clock = pygame.time.Clock()
    running = True

    planets = generate_planets(num_planets=10, world_size=(6000, 6000))
    player_x, player_y = spawn_on_planet(planets[0], 270)
    spaceship_x, spaceship_y = spawn_on_planet(planets[0], 270) 
    player = Player(player_x, player_y, mass=1, radius=2)
    spaceship = Spaceship(planet=planets, x=spaceship_x, y=spaceship_y, mass=100, radius=10)
    camera = Camera(player.position, window_size[0], window_size[1])

    time_var = 0
    start_time = time.time()

    # Track discovered planets and message timing
    discovery_message = None
    discovery_timer = 0  

    show_debug = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False

        dt = clock.tick(60) / 1000.0
        time_var += dt
        keys = pygame.key.get_pressed()

        # Update game objects
        player.update(dt, planets, spaceship)
        spaceship.update(dt, keys, planets, player)
        
        # Determine the entity the camera is following (player or spaceship)
        camera_target = player if not player.in_ship else spaceship

        # Update the camera
        camera.update(camera_target)

        # Adjust zoom based on the target's distance to the nearest planet
        distance, closest_planet = distance_to_nearest_planet(camera_target, planets)
        adjust_zoom_based_on_distance(camera, distance, player)

        # Clear the screen
        screen.fill((0, 0, 0))
        transparent_surface = pygame.Surface(window_size, pygame.SRCALPHA)

        # Handle player input
        handle_keys(player, closest_planet, keys, spaceship, ui, camera, dt)

        # Handle collisions between player and fuel tanks
        for planet in planets:
            for tank in planet.fuel_tanks:
                if (tank.position - player.position).length() < tank.radius + player.radius:
                    tank.refill(spaceship)
                    planet.fuel_tanks.remove(tank)  # Remove the tank after refilling


        # Draw game objects
        for planet in planets:
            planet.draw(screen, transparent_surface, camera, time_var, player.position)

        #not in ship
        if not player.in_ship: 
            player.draw(screen, camera)
            #player boost bar 
            ui.draw_bar(player.fuel, player.max_fuel, 200, 0, ("left", "top"))

            if time.time() - start_time < 5:
                prompt_position = camera.apply(player) + pygame.math.Vector2(20, -20)
                ui.draw_prompt("WASD to move", prompt_position, time)

        #In ship 
        else:
            #ship boost bar
            ui.draw_bar(spaceship.boost_cylinder_amount, spaceship.boost_cylinder_capacity, 200, 0, ("left", "top"))
            #ship oxygen bar
            ui.draw_bar(spaceship.oxygen_amount, spaceship.max_oxygen, 100, 1, ("left", "top"))

        #ship fuel bar
        ui.draw_bar(spaceship.fuel_amount, spaceship.max_fuel, 100, 1, ("right", "top"))

        spaceship.draw(screen, camera)

        screen.blit(transparent_surface, (0, 0))

        
        # Draw game objects
        for planet in planets:
            planet.draw(screen, transparent_surface, camera, time_var, player.position)

        # Update discovered planets
        for planet in planets:

            if planet.discovered == False:
                if (player.position - planet.position).length() < (planet.radius + 200):
                    planet.discovered = True
                    discovery_message = "Map Updated"
                    discovery_timer = time.time()  # Start timer


        spaceship.draw(screen, camera)

        # Draw the mini-map
        ui.draw_map(screen, player, spaceship, planets)

        for planet in planets:
            if ((player.position - planet.position).length() >= (planet.radius + 100)) and ((player.position - planet.position).length() < 2000 and planet.discovered == False):
                ui.draw_planet_indicators(screen, camera, planet)

        # Display discovery message for 3 seconds
        if discovery_message and (time.time() - discovery_timer < 1):
            ui.draw_discovery_message(screen, discovery_message)
        elif discovery_message:
            discovery_message = None  # Clear message after 3 seconds

        if time.time() - start_time < 3:
            screen.fill((0, 0, 0))

        if spaceship.oxygen_amount <= 0:
            ui.show_message("Oxygen Depleted. Game Over")
            main()  # Restart the game

        if keys[pygame.K_p]:
            
            show_debug = not show_debug

        if show_debug:
            ui.display_debug(screen, spaceship, planets, player)

        pygame.display.flip()

            
    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    main()



