import pygame
import anchors
import savedata
from buttons import TextButton

# init pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()
savedata.init()

# game setup
screen = pygame.display.set_mode((1000, 1000))
screen_rect = screen.get_rect()
clock = pygame.time.Clock()
saves_index = savedata.load_index()
running = True


# fonts setup
TEXT_SIZE_BASE = 30
MAIN_FONT_FILE = "assets/fonts/windows_command_prompt.ttf"
main_font_base = pygame.font.Font(MAIN_FONT_FILE, TEXT_SIZE_BASE)


# main menu finite state machine
INTRO = 0
TITLE = 1
MAIN_MENU = 2
NEW_GAME_MENU = 3
LOAD_GAME_MENU = 4
main_menu_current_state = INTRO
main_menu_current_state_started = 0
main_menu_current_state_first_tick = False
main_menu_music_playing = False


# intro screen state
background = pygame.Surface(screen_rect.size)
ucab_logo = pygame.image.load("assets/sprites/titlescreen/ucab_logo.png")
ucab_logo = pygame.transform.scale(ucab_logo, (500, 500))
ucab_logo_draw_rect = pygame.rect.Rect(screen_rect.centerx - 250, screen_rect.centery - 250, 500, 500)
pygame_logo = pygame.image.load("assets/sprites/titlescreen/pygame_logo.png")
pygame_logo_og_rect = pygame_logo.get_rect()
pygame_logo_draw_width = screen_rect.width / 3 * 2
pygame_logo_draw_height = pygame_logo_draw_width * pygame_logo_og_rect.height / pygame_logo_og_rect.width
pygame_logo_draw_rect = pygame.rect.Rect((screen_rect.centerx - pygame_logo_draw_width / 2, screen_rect.centery - pygame_logo_draw_height / 2), (pygame_logo_draw_width, pygame_logo_draw_height))
pygame_logo = pygame.transform.scale(pygame_logo, pygame_logo_draw_rect.size)
intro_music = pygame.mixer.Sound("assets/sfx/titlescreen/konami_intro.mp3")
intro_music_playing = False


# title screen
title_sprite = pygame.image.load("assets/sprites/titlescreen/title.png")
title_og_rect = title_sprite.get_rect()
title_draw_height = screen_rect.width * title_og_rect.height / title_og_rect.width
title_draw_rect = pygame.rect.Rect(0, screen_rect.height / 3 - title_draw_height / 2, screen_rect.width, title_draw_height)
title_sprite = pygame.transform.scale(title_sprite, title_draw_rect.size)
title_button_text_color_base = "#e2d6b8"
title_button_text_color_selected = "#fff0b3"
title_button_anchor_center = pygame.Vector2(screen_rect.centerx, screen_rect.height / 3 * 2)
LOCALE_PRESSANYBUTTON = "PRESS ANY BUTTON"
title_button_pressanybutton = TextButton(LOCALE_PRESSANYBUTTON, main_font_base, title_button_text_color_base, title_button_text_color_selected, title_button_anchor_center + (0, 44*3), anchors.middle_center)


# main menu screen
LOCALE_NEWGAME = "NEW GAME"
LOCALE_LOADGAME = "LOAD GAME"
LOCALE_CONTINUE = "CONTINUE"
LOCALE_QUIT = "QUIT"
title_buttons_offset = 44
title_button_continue = TextButton(LOCALE_CONTINUE, main_font_base, title_button_text_color_base, title_button_text_color_selected, title_button_anchor_center, anchors.middle_center)
title_button_loadgame = TextButton(LOCALE_LOADGAME, main_font_base, title_button_text_color_base, title_button_text_color_selected, title_button_anchor_center + (0, title_buttons_offset), anchors.middle_center)
title_button_newgame = TextButton(LOCALE_NEWGAME, main_font_base, title_button_text_color_base, title_button_text_color_selected, title_button_anchor_center + (0, title_buttons_offset*2), anchors.middle_center)
title_button_quit = TextButton(LOCALE_QUIT, main_font_base, title_button_text_color_base, title_button_text_color_selected, title_button_anchor_center + (0, title_buttons_offset*3), anchors.middle_center)
main_menu_button_cursor = 0
main_menu_buttons = []
main_menu_game_start_sfx = pygame.mixer.Sound("assets/sfx/titlescreen/game_start.mp3")
main_menu_button_select_sfx = pygame.mixer.Sound("assets/sfx/titlescreen/button_select.mp3")


# load menu screen
LOCALE_VAGABOND = "VAGABOND"
LOCALE_ASTROLOGER = "ASTROLOGER"
LOCALE_PRISONER = "PRISONER"
new_game_bg = pygame.image.load("assets/sprites/menus/new_game_bg.png")
new_game_bg = pygame.transform.scale(new_game_bg, screen_rect.size)
new_game_class_cursor = 0
new_game_class_portrait_width = 200
new_game_class_vagabond_portrait = pygame.image.load("assets/sprites/menus/vagabond.png")
new_game_class_vagabond_portrait_og_rect = new_game_class_vagabond_portrait.get_rect()
new_game_class_vagabond_portrait_draw_width = new_game_class_portrait_width * 1.5
new_game_class_vagabond_portrait_draw_height = new_game_class_portrait_width * 1.5 * new_game_class_vagabond_portrait_og_rect.height / new_game_class_vagabond_portrait_og_rect.width
new_game_class_vagabond_portrait_draw_rect = pygame.rect.Rect((screen_rect.centerx / 2 - new_game_class_vagabond_portrait_draw_width / 2 - 60, screen_rect.centery - new_game_class_vagabond_portrait_draw_height / 2 - 15), (new_game_class_vagabond_portrait_draw_width, new_game_class_vagabond_portrait_draw_height))
new_game_class_vagabond_portrait = pygame.transform.scale(new_game_class_vagabond_portrait, new_game_class_vagabond_portrait_draw_rect.size)
new_game_class_astrologer_portrait = pygame.image.load("assets/sprites/menus/astrologer.png")
new_game_class_astrologer_portrait_og_rect = new_game_class_astrologer_portrait.get_rect()
new_game_class_astrologer_portrait_draw_width = new_game_class_portrait_width
new_game_class_astrologer_portrait_draw_height = new_game_class_portrait_width * new_game_class_astrologer_portrait_og_rect.height / new_game_class_astrologer_portrait_og_rect.width
new_game_class_astrologer_portrait_draw_rect = pygame.rect.Rect((screen_rect.centerx - new_game_class_astrologer_portrait_draw_width / 2, screen_rect.centery - new_game_class_astrologer_portrait_draw_height / 2), (new_game_class_astrologer_portrait_draw_width, new_game_class_astrologer_portrait_draw_height))
new_game_class_astrologer_portrait = pygame.transform.scale(new_game_class_astrologer_portrait, (new_game_class_portrait_width, new_game_class_portrait_width * new_game_class_astrologer_portrait_og_rect.height / new_game_class_astrologer_portrait_og_rect.width))
new_game_class_prisoner_portrait = pygame.image.load("assets/sprites/menus/prisoner.png")
new_game_class_prisoner_portrait_og_rect = new_game_class_prisoner_portrait.get_rect()
new_game_class_prisoner_portrait_draw_width = new_game_class_portrait_width
new_game_class_prisoner_portrait_draw_height = new_game_class_portrait_width * new_game_class_prisoner_portrait_og_rect.height / new_game_class_prisoner_portrait_og_rect.width
new_game_class_prisoner_portrait_draw_rect = pygame.rect.Rect((screen_rect.right * 3 / 4 - new_game_class_prisoner_portrait_draw_width / 2 + 30, screen_rect.centery - new_game_class_prisoner_portrait_draw_height / 2), (new_game_class_prisoner_portrait_draw_width, new_game_class_prisoner_portrait_draw_height))
new_game_class_prisoner_portrait = pygame.transform.scale(new_game_class_prisoner_portrait, (new_game_class_portrait_width, new_game_class_portrait_width * new_game_class_prisoner_portrait_og_rect.height / new_game_class_prisoner_portrait_og_rect.width))


# load menu screen
load_menu_options = []



# game loop
while running:
    # setting up game times
    current_ticks = pygame.time.get_ticks()

    # setting up key press detection
    keys = pygame.key.get_pressed()
    keys_down = {}

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys_down[event.key] = True

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")


    if main_menu_current_state == INTRO:
        intro_ticks = current_ticks - main_menu_current_state_started

        if not intro_music_playing:
            intro_music.play()
            intro_music_playing = True

        if intro_ticks > 2900 and intro_ticks < 3400:
            alpha = (intro_ticks - 2900) % 500 * 255 / 500
            background.set_alpha(alpha)
            background.fill("white")
            screen.blit(background, (0, 0))
            ucab_logo.set_alpha(alpha)
            screen.blit(ucab_logo, ucab_logo_draw_rect)

        if intro_ticks > 3400 and intro_ticks < 7100:
            background.set_alpha(255)
            background.fill("white")
            screen.blit(background, (0, 0))
            ucab_logo.set_alpha(255)
            screen.blit(ucab_logo, ucab_logo_draw_rect)

        if intro_ticks > 7100 and intro_ticks < 7600:
            alpha = 255 - (intro_ticks - 7100) % 500 * 255 / 500
            background.set_alpha(alpha)
            background.fill("white")
            screen.blit(background, (0, 0))
            ucab_logo.set_alpha(alpha)
            screen.blit(ucab_logo, ucab_logo_draw_rect)

        if intro_ticks > 8400 and intro_ticks < 8900:
            alpha = (intro_ticks - 8400) % 500 * 255 / 500
            pygame_logo.set_alpha(alpha)
            screen.blit(pygame_logo, pygame_logo_draw_rect)

        if intro_ticks > 8900 and intro_ticks < 12600:
            pygame_logo.set_alpha(255)
            screen.blit(pygame_logo, pygame_logo_draw_rect)

        if intro_ticks > 12600 and intro_ticks < 13100:
            alpha = 255 - (intro_ticks - 12600) % 500 * 255 / 500
            pygame_logo.set_alpha(alpha)
            screen.blit(pygame_logo, pygame_logo_draw_rect)
        
        if intro_ticks > 14000 or len(keys_down) > 0:
            main_menu_current_state = TITLE
            main_menu_current_state_started = current_ticks
            intro_music.stop()
    

    elif main_menu_current_state == TITLE:
        title_ticks = current_ticks - main_menu_current_state_started

        if len(keys_down) > 0:
            main_menu_current_state = MAIN_MENU
            main_menu_current_state_started = current_ticks
            main_menu_current_state_first_tick = True

        title_button_pressanybutton.selected = True
        screen.blit(title_sprite, title_draw_rect.topleft)

        if title_ticks < 2000:
            alpha = 255 - title_ticks % 2000 * 255 / 2000
            background.set_alpha(alpha)
            background.fill("black")
            screen.blit(background, (0, 0))
        else:
            if (title_ticks - 2000) // 750 % 2 == 0:
                title_button_pressanybutton.draw(screen)

            if not main_menu_music_playing:
                pygame.mixer.music.load("assets/music/main_theme.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(1)
                main_menu_music_playing = True

    
    elif main_menu_current_state == MAIN_MENU:
        if main_menu_current_state_first_tick:
            saves_index = savedata.load_index()
            if len(saves_index["saves"]) > 0:
                main_menu_buttons = [title_button_continue, title_button_loadgame, title_button_newgame, title_button_quit]
            else:
                main_menu_buttons = [title_button_newgame, title_button_quit]
            main_menu_current_state_first_tick = False

        if not main_menu_music_playing:
            pygame.mixer.music.load("assets/music/main_theme.mp3")
            pygame.mixer.music.play(-1)
            main_menu_music_playing = True

        if keys_down.get(pygame.K_UP) or keys_down.get(pygame.K_w):
            main_menu_button_cursor = main_menu_button_cursor - 1
            main_menu_button_select_sfx.play()
        if keys_down.get(pygame.K_DOWN) or keys_down.get(pygame.K_s):
            main_menu_button_cursor = main_menu_button_cursor + 1
            main_menu_button_select_sfx.play()
        main_menu_button_cursor = main_menu_button_cursor % len(main_menu_buttons)

        for i, button in enumerate(main_menu_buttons):
            button.selected = main_menu_button_cursor == i
            button.draw(screen)
        
        if keys_down.get(pygame.K_RETURN) or keys_down.get(pygame.K_SPACE):
            if title_button_newgame:
                main_menu_current_state = NEW_GAME_MENU
                main_menu_current_state_started = current_ticks
                main_menu_music_playing = False
                pygame.mixer.music.stop()
            if title_button_quit.selected:
                running = False
            if title_button_continue.selected:
                pygame.mixer.music.stop()
                main_menu_game_start_sfx.play()
                
        screen.blit(title_sprite, title_draw_rect.topleft)


    elif main_menu_current_state == NEW_GAME_MENU:
        screen.blit(new_game_bg, (0, 0))
        screen.blit(new_game_class_vagabond_portrait, new_game_class_vagabond_portrait_draw_rect)
        screen.blit(new_game_class_astrologer_portrait, new_game_class_astrologer_portrait_draw_rect)
        screen.blit(new_game_class_prisoner_portrait, new_game_class_prisoner_portrait_draw_rect)


    elif main_menu_current_state == LOAD_GAME_MENU:
        pass


    # debugging controls
    if keys[pygame.K_LSHIFT] and keys_down.get(pygame.K_ESCAPE):
        running = False
    if keys_down.get(pygame.K_F1):
        main_menu_current_state = INTRO
        main_menu_current_state_started = current_ticks
        intro_music.stop()
        intro_music_playing = False
        main_menu_music_playing = False
        pygame.mixer.music.stop()
    if keys_down.get(pygame.K_F2):
        main_menu_current_state = TITLE
        main_menu_current_state_started = current_ticks
        main_menu_music_playing = False
        pygame.mixer.music.stop()
    if keys_down.get(pygame.K_F3):
        main_menu_current_state = MAIN_MENU
        main_menu_current_state_started = current_ticks
        main_menu_music_playing = False
        main_menu_current_state_first_tick = True
        pygame.mixer.music.stop()


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()