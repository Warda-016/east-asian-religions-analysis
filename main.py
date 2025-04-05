# Import required libraries
import pygame  # Pygame for game development
import time  # Time module to track elapsed time
import random  # Random module (can be used for obstacles or other features)

# Initialize fonts in Pygame
pygame.font.init()

# Define screen dimensions
width, height = 1000, 600

# Define player attributes
player_width = 40
player_height = 60
player_velocity = 5  # Speed at which player moves
star_width = 20
star_height = 30
star_velocity =5

# Create game window
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Dodge")  # Set window title

# Load and scale background image to fit the screen
bg = pygame.transform.scale(pygame.image.load("bg.jpg"), (width, height))
# Load and scale player and meteor images
player_img = pygame.transform.scale(pygame.image.load("player.png"), (player_width, player_height))
meteor_img = pygame.transform.scale(pygame.image.load("meteor.png"), (star_width, star_height))


# Initialize font for displaying text
font = pygame.font.SysFont("comicsans", 30)

# Function to draw game elements on the screen
def draw(player, elapsed_time, stars, lives, stars_dodged):
    win.blit(bg, (0,0))  # Draw background image

    # Render the elapsed time text
    time_text = font.render(f"Time: {round(elapsed_time)}s", 1, "white")
    win.blit(time_text, (10,10))  # Display time text at top-left corner

    # Lives text
    lives_text = font.render(f"Lives: {lives}", 1, "white")
    win.blit(lives_text, (10, 40))

    # show stars dodged
    score_text = font.render(f"Score: {stars_dodged}", 1, "white")
    win.blit(score_text, (10, 70))


    # Draw the player rectangle
    win.blit(player_img, (player.x, player.y))

    #draw a star
    for star in stars:
        win.blit(meteor_img, (star.x, star.y))

    pygame.display.update()  # Update display

    # start screen or instructions function
def start_screen():
    waiting = True

    while waiting:
        win.blit(bg, (0, 0))  # Draw background

        # Title text
        title_text = font.render("SPACE DODGE", True, "white")
        win.blit(title_text, (width//2 - title_text.get_width()//2, height//3))

        # Instruction text
        instruct_text = font.render("Use ← → arrow keys to move", True, "white")
        win.blit(instruct_text, (width//2 - instruct_text.get_width()//2, height//2))

        # Press to start
        start_text = font.render("Press any key to start", True, "yellow")
        win.blit(start_text, (width//2 - start_text.get_width()//2, height//1.5))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False



# Main game loop function
def main():
    start_screen()  # Show menu screen before game starts
    run = True  # Game running flag

    # Create player rectangle (x, y, width, height)
    player = pygame.Rect(200, height - player_height, 
                         player_width, player_height)

    clock = pygame.time.Clock()  # Create clock object to control frame rate
    start_time = time.time()  # Store the time when game starts
    elapsed_time=0

    star_add_increment = 2000
    star_count = 0 #it will tell when we should add the next stop or start

    stars  = []
    hit = False

    lives = 3  # Player has 3 lives
    score = 0  # score based on time or stars dodged
    stars_dodged = 0

    # Timer for star spawning using pygame's clock (fixes star not appearing)
    star_timer = pygame.time.get_ticks()  # Stores time of last star spawn

    while run:
        star_count = clock.tick(60) #clock.tick returns the number of miliseconds since the last clock tick
        elapsed_time = time.time() - start_time  # Calculate elapsed time

        #generated all of the stars
        # ✅ FIXED: Now using actual elapsed time to check if it's time to add stars
        if pygame.time.get_ticks() - star_timer > star_add_increment:
            for _ in range(3): # _ is a plceholder and has the same purpose as that of i
                star_x = random.randint(0, width - star_width )
                star = pygame.Rect(star_x, -star_height, star_width, star_height)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_timer = pygame.time.get_ticks()  # ✅ Reset star spawn timer

        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If user clicks the close button, exit loop
                run = False
                break

        # Get keyboard input
        keys = pygame.key.get_pressed()
        
        # Move player left if Left Arrow key is pressed and within screen bounds
        if keys[pygame.K_LEFT] and player.x - player_velocity >= 0:
            player.x -= player_velocity
        
        # Move player right if Right Arrow key is pressed and within screen bounds
        if keys[pygame.K_RIGHT] and player.x + player_velocity + player.width <= width:
            player.x += player_velocity
        
        # Move all the stars
        for star in stars[:]:
            star.y += star_velocity

            if star.y > height:
                stars.remove(star)
                stars_dodged += 1  # Count when a star is successfully dodged

            elif star.colliderect(player):  # Simplified and improved
                stars.remove(star)
                lives -= 1  # 👈 Lose a life on hit
                if lives <= 0:
                    hit = True
                break  # Exit loop for this frame

        if hit:
            lost_text = font.render("You lost!", 1, "red")  #generate text
            win.blit(lost_text, (width/2-lost_text.get_width()/2, height/2-lost_text.get_height()/2)) #draw it on the screen
            pygame.display.update()
            pygame.time.delay(4000) #delatying everything for a few miliseconds, so u can see the text on scrn
            break

        draw(player, elapsed_time, stars, lives, stars_dodged)  # Update the screen with new positions

    pygame.quit()  # Quit the game when loop ends

# Run the game if this file is executed directly
if __name__ == "__main__":
    main()
