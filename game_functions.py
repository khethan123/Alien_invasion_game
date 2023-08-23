import sys  
# It's only required in this module so not required in other modules
import pygame

from alien import Alien
from bullet import Bullet
from time import sleep

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Responding to key presses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # (close program 'X')
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # (keybord inputs)
            check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:  # (no i/p)
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets , mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets , mouse_x, mouse_y):
    """Start a new game when the player clicks play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active :
        # The above line checks if play button and mouse click are overlapping or not.
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Responds to key presses."""
    if (event.key == pygame.K_KP_6) or (event.key == pygame.K_RIGHT):
        ship.moving_right = True
    if (event.key == pygame.K_KP_4) or (event.key == pygame.K_LEFT):
        ship.moving_left = True
    if (event.key == pygame.K_KP_8) or (event.key == pygame.K_UP):
        ship.moving_up = True
    if (event.key == pygame.K_KP_2) or (event.key == pygame.K_DOWN):
        ship.moving_down = True
    if event.key == pygame.K_c: # (auto centering)
        ship.moving_center = True
    if event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    """Respond to key releases."""
    if (event.key == pygame.K_KP_6) or (event.key == pygame.K_RIGHT):
        ship.moving_right = False
    if (event.key == pygame.K_KP_4) or (event.key == pygame.K_LEFT):
        ship.moving_left = False
    if (event.key == pygame.K_KP_8) or (event.key == pygame.K_UP):
        ship.moving_up = False
    if (event.key == pygame.K_KP_2) or (event.key == pygame.K_DOWN):
        ship.moving_down = False

def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
        # Hide mouse button
        pygame.mouse.set_visible(0)
        # Reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Update the images on the screen & flip to the new screen."""
    # Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)
    
    # Redraw all bullets behind ship and alliens
    for bullet in bullets.sprites():
        bullet.draw_bullets()

    ship.blitme()
    aliens.draw(screen)

    # Draw the score information
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, bullets, aliens):
    """Updating the position of bullets and getting rid of old bullets."""
    # First update bullet position
    bullets.update()

    # Getting rid of ones that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.top <= 0: 
            bullets.remove(bullet)
   
    check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, bullets, aliens)

def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, bullets, aliens):
    """Respond ot bullet alien collision."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # IF the entire fleet is desctroyed, start a new level.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if the limit is not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_of_aliens(ai_settings, alien.rect.width) 
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
        # Create an alien and place it in the row.
            create_alien(ai_settings, screen, aliens, alien_number, alien.rect.width, 
                         row_number, alien.rect.height)

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = ai_settings.screen_height - (20 * alien_height) - (3 * ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def get_number_of_aliens(ai_settings, alien_width):
    "Determine the number of A that fit in a row."
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, alienwidth, row_number,
                  alienheight):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien.x = alienwidth + 2 * alienwidth * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alienheight * 4 + 2 * alienheight * row_number
    aliens.add(alien)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any alien has reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change its direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, bullets, aliens):
    """Respond to ship being hit by the alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1

        # Update Scoreboard
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause 
        sleep(0.5)
    
    else:
        stats.game_active = False
        pygame.mouse.set_visible(1)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, bullets, aliens):
    """Check if aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat it the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, bullets, aliens)

def update_aliens(ai_settings, screen, stats, sb, ship, bullets, aliens):
    """
    Check if the fleet is at an edge, 
     update the positions of all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, bullets, aliens)

    # Look for aliens hitting the bottom of the scree
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, bullets, aliens)

def check_high_score(stats, sb):
    """Check to see if there is a new high score."""
    if stats.score > stats.high_scores:
        stats.high_scores = stats.score
        sb.prep_high_score()