import pygame 
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Marvel Heroes Battle")
BACKGROUND_COLOR = (30, 30, 60)
WHITE = (255, 255, 255)
HIGHLIGHT_COLOR = (255, 215, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game settings
FPS = 60
clock = pygame.time.Clock()
SPRITE_WIDTH, SPRITE_HEIGHT = 150, 150  # Increased sprite size

# Character data
characters = [
    {"name": "Spider-Man", "sprite": "images/spiderman.png", "speed": 7, "attack": 8, "special": "Web Swing"},
    {"name": "Iron Man", "sprite": "images/ironman.png", "speed": 6, "attack": 10, "special": "Repulsor Beam"},
    {"name": "Hulk", "sprite": "images/hulk.png", "speed": 5, "attack": 12, "special": "Hulk Smash"},
    {"name": "Thor", "sprite": "images/thor.png", "speed": 6, "attack": 11, "special": "Thunder Strike"},
    {"name": "Iceman", "sprite": "images/iceman.png", "speed": 5, "attack": 10, "special": "Frost Barrier"},
    {"name": "Thanos", "sprite": "images/thanos.png", "speed": 7, "attack": 15, "special": "Infinity Gauntlet"},
    {"name": "Doctor Strange", "sprite": "images/doctor_strange.png", "speed": 7, "attack": 12, "special": "Eye of Agamotto"},
    {"name": "Mystique", "sprite": "images/mystique.png", "speed": 13, "attack": 10, "special": "Shape Shift"},
    {"name": "Wolverine", "sprite": "images/wolverine.png", "speed": 12, "attack": 15, "special": "Berserker Rage"},
    {"name": "Deadpool", "sprite": "images/deadpool.png", "speed": 12, "attack": 15, "special": "Regeneration"},
    {"name": "Quicksilver", "sprite": "images/quicksilver.png", "speed": 20, "attack": 15, "special": "Blazing Speed"},
    {"name": "Venom", "sprite": "images/venom.png", "speed": 12, "attack": 15, "special": "Symbiote Tendrils"},
]

villains = {
    "Loki": {"sprite": "images/loki.png", "speed": 6, "attack": 10, "special": "Illusion"},
    "Ultron": {"sprite": "images/ultron.png", "speed": 8, "attack": 12, "special": "Energy Blast"},
    "Hela": {"sprite": "images/hela.png", "speed": 7, "attack": 13, "special": "Necroswords"},
    "Green Goblin": {"sprite": "images/green_goblin.png", "speed": 7, "attack": 11, "special": "Pumpkin Bombs"}
}

# Load character images
menu_images = {}
for char in characters:
    try:
        image = pygame.image.load(char["sprite"])
        menu_images[char["name"]] = pygame.transform.scale(image, (SPRITE_WIDTH, SPRITE_HEIGHT))
    except pygame.error:
        print(f"Error loading image for {char['name']}: {char['sprite']}")

# Fonts
font = pygame.font.Font(None, 50)  # Increased font size for better visibility
stats_font = pygame.font.Font(None, 40)  # Increased font size for stats

# Character selection screen
def character_selection():
    selected_index = 0
    names = [char["name"] for char in characters]
    total_characters = len(names)
    cols = 4  # Number of columns
    rows = (total_characters // cols) + (total_characters % cols > 0)  # Calculate rows needed

    while True:
        screen.fill(BACKGROUND_COLOR)

        # Title
        title = font.render("Hero Selection", True, WHITE)
        screen.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 80))

        # Calculate the starting X and Y to center the character grid
        grid_spacing_x = 50  # Increased spacing for clarity
        grid_spacing_y = 80
        grid_width = cols * (SPRITE_WIDTH + grid_spacing_x) - grid_spacing_x
        grid_height = rows * (SPRITE_HEIGHT + grid_spacing_y) - grid_spacing_y
        start_x = (SCREEN_WIDTH - grid_width) // 2
        start_y = (SCREEN_HEIGHT - grid_height) // 2 + 80

        # Draw character menu centered on screen
        for i, name in enumerate(names):
            x = start_x + (i % cols) * (SPRITE_WIDTH + grid_spacing_x)
            y = start_y + (i // cols) * (SPRITE_HEIGHT + grid_spacing_y)
            if name == names[selected_index]:
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, (x - 20, y - 20, SPRITE_WIDTH + 40, SPRITE_HEIGHT + 40), 3)
            screen.blit(menu_images[name], (x, y))

        selected_text = font.render(f"Selected: {names[selected_index]}", True, HIGHLIGHT_COLOR)
        screen.blit(selected_text, ((SCREEN_WIDTH - selected_text.get_width()) // 2, SCREEN_HEIGHT - 150))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and selected_index > 0:
            selected_index -= 1
            pygame.time.delay(100)  # Reduced delay for faster navigation
        if keys[pygame.K_RIGHT] and selected_index < len(names) - 1:
            selected_index += 1
            pygame.time.delay(100)
        if keys[pygame.K_RETURN]:
            return names[selected_index]

        pygame.display.flip()
        clock.tick(FPS)

# Collision detection
def detect_collision(player_rect, villain_rect):
    return player_rect.colliderect(villain_rect)

# Special move implementation
def use_special_move(character, opponent):
    special = character["special"]
    damage = 0
    if special == "Web Swing":
        damage = 25
    elif special == "Repulsor Beam":
        damage = 30
    elif special == "Hulk Smash":
        damage = 40
    elif special == "Thunder Strike":
        damage = 35
    opponent["health"] = max(0, opponent["health"] - damage)

# Draw health bar
def draw_health_bar(x, y, health, max_health):
    ratio = max(0, health / max_health)
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 250, 30))
    pygame.draw.rect(screen, (0, 255, 0), (x, y, int(250 * ratio), 30))

# Draw energy bar
def draw_energy_bar(x, y, energy, max_energy):
    ratio = max(0, energy / max_energy)
    pygame.draw.rect(screen, BLUE, (x, y, 250, 30))
    pygame.draw.rect(screen, CYAN, (x, y, int(250 * ratio), 30))

# Timer display
def draw_timer(x, y, time_left):
    timer_text = font.render(f"Time: {time_left}s", True, WHITE)
    screen.blit(timer_text, (x, y))

# Round info display
def draw_round_info(round_number, player_wins, villain_wins):
    round_text = font.render(f"Round: {round_number}/3", True, WHITE)
    player_score_text = font.render(f"Player Wins: {player_wins}", True, GREEN)
    villain_score_text = font.render(f"Villain Wins: {villain_wins}", True, RED)
    screen.blit(round_text, (SCREEN_WIDTH // 2 - 150, 10))
    screen.blit(player_score_text, (50, 10))
    screen.blit(villain_score_text, (SCREEN_WIDTH - 350, 10))

# Main game loop
def game_loop():
    player_name = character_selection()
    villain_name = random.choice(list(villains.keys()))

    player_data = next(c for c in characters if c["name"] == player_name)
    villain_data = villains[villain_name]

    player_sprite = pygame.image.load(player_data["sprite"])
    player_sprite = pygame.transform.scale(player_sprite, (SPRITE_WIDTH, SPRITE_HEIGHT))

    villain_sprite = pygame.image.load(villain_data["sprite"])
    villain_sprite = pygame.transform.scale(villain_sprite, (SPRITE_WIDTH, SPRITE_HEIGHT))

    total_rounds = 3
    current_round = 1
    player_wins = 0
    villain_wins = 0

    while current_round <= total_rounds:
        player_health, villain_health = 100, 100
        player_energy, villain_energy = 0, 0
        max_energy = 100

        player_x, player_y = 200, SCREEN_HEIGHT - SPRITE_HEIGHT - 50
        villain_x, villain_y = SCREEN_WIDTH - 300, SCREEN_HEIGHT - SPRITE_HEIGHT - 50

        time_left = 60
        pygame.time.set_timer(pygame.USEREVENT, 1000)

        running = True
        while running:
            screen.fill(BACKGROUND_COLOR)
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.USEREVENT:
                    time_left -= 1
                    if time_left <= 0:
                        running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_data["speed"]
            if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - SPRITE_WIDTH:
                player_x += player_data["speed"]
            if keys[pygame.K_UP] and player_y > 0:
                player_y -= player_data["speed"]
            if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - SPRITE_HEIGHT:
                player_y += player_data["speed"]

            player_rect = pygame.Rect(player_x, player_y, SPRITE_WIDTH, SPRITE_HEIGHT)
            villain_rect = pygame.Rect(villain_x, villain_y, SPRITE_WIDTH, SPRITE_HEIGHT)

            if keys[pygame.K_SPACE] and detect_collision(player_rect, villain_rect):
                villain_health -= player_data["attack"]

            if keys[pygame.K_s] and player_energy >= max_energy and detect_collision(player_rect, villain_rect):
                use_special_move(player_data, {"health": villain_health})
                player_energy = 0

            if villain_x > player_x:
                villain_x -= villain_data["speed"]
            elif villain_x < player_x:
                villain_x += villain_data["speed"]

            if detect_collision(player_rect, villain_rect) and random.random() < 0.02:
                player_health -= villain_data["attack"]
                villain_energy += 10

            if random.random() < 0.01 and villain_energy >= max_energy and detect_collision(player_rect, villain_rect):
                use_special_move(villain_data, {"health": player_health})
                villain_energy = 0

            if player_health <= 0 or villain_health <= 0:
                running = False

            draw_health_bar(50, 50, player_health, 100)
            draw_health_bar(SCREEN_WIDTH - 300, 50, villain_health, 100)
            draw_energy_bar(50, 80, player_energy, max_energy)
            draw_energy_bar(SCREEN_WIDTH - 300, 80, villain_energy, max_energy)
            draw_timer(SCREEN_WIDTH // 2 - 75, 50, time_left)
            draw_round_info(current_round, player_wins, villain_wins)

            screen.blit(player_sprite, (player_x, player_y))
            screen.blit(villain_sprite, (villain_x, villain_y))

            pygame.display.flip()

        if player_health > 0:
            player_wins += 1
        else:
            villain_wins += 1

        current_round += 1

    screen.fill(BLACK)
    winner = player_name if player_wins > villain_wins else villain_name

   # Display the winner at the top and larger hero image in the center
    winner_data = player_data if player_wins > villain_wins else villain_data
    winner_sprite = pygame.image.load(winner_data["sprite"])
    winner_sprite = pygame.transform.scale(winner_sprite, (SPRITE_WIDTH * 3, SPRITE_HEIGHT * 3))  # Larger image

    end_text = font.render(f"Winner: {winner}", True, WHITE)
    result_text = font.render(f"Result: {player_wins}-{villain_wins}", True, WHITE)

    # Blit result text at the top
    screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, 50))
    screen.blit(result_text, (SCREEN_WIDTH // 2 - result_text.get_width() // 2, 100))
    screen.blit(winner_sprite, (SCREEN_WIDTH // 2 - winner_sprite.get_width() // 2, SCREEN_HEIGHT // 2 - winner_sprite.get_height() // 2))
    pygame.display.flip()

    pygame.time.delay(3000)  # Display the result for a few seconds before quitting

# Run the game
game_loop()
pygame.quit()
