import pygame
import sys
import random
import time
import math
import pygame.freetype

words_file_name = "words_alpha.txt"
# If a word has a white space character such as " ", only take the first part of the string and discard the part
# after the white space character
with open(words_file_name, 'r', encoding='utf-8') as f:
    dictionary = [line.strip().split()[0] for line in f]

word_count = len(dictionary)

# Initialize pygame
pygame.init()

# Set the window size and caption
size_x = 1920
size_y = 1080
size = (size_x, size_y)
caption = "Typing Game"
screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
pygame.display.set_caption(caption)

pause_key = pygame.K_ESCAPE

# Create a font object
font = pygame.font.Font("Roboto-Regular.ttf", 32)

correct_words = 0
wrong_words = 0
game_time = 60  # time in seconds
# TODO: End screen to display score
endless_game = True
paused = False

# Create a string variable to store the text in the input area
input_text = ""
remaining_words_readable = ""

random_choice = True

red_color = (255, 0, 0)
green_color = (0, 255, 0)
dictionary_end = False


# input, current_word
def matching_part(string1, string2):
    if not string1 or not string2:
        # if not string1:
        #     print("empty input")
        # if not string2:
        #     print("empty word")
        return 0
    if string2.startswith(string1):
        # print(f"returning {len(string1[:len(string2)])}")
        return len(string1[:len(string2)])
    else:
        # print(f"No match: {string1} vs {string2}")
        return 0


def update_remaining_words_readable():
    global remaining_words_readable
    remaining_words_readable = ""
    if len(dictionary) > 0:
        index = 0
        for word in dictionary:
            remaining_words_readable += word + ", "
            index += 1
            if index > 7:
                break


def check_input(input, word):
    if input == word:
        return True
    elif input == "cheating":
        print(f"Cheat code")
        return True
    else:
        return False


def pick_next_word():
    global dictionary
    if len(dictionary) < 1:
        return False

    random_word = dictionary[0]
    update_remaining_words_readable()
    dictionary.remove(random_word)

    return random_word


# print('\u200c')

if random_choice:
    print(f"Shuffled words")
    random.shuffle(dictionary)

current_word = pick_next_word()
print(f"Current word: {current_word}")
# Display the correct part green, wrong part red
green_index = 0

start_time = time.time()

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Pause game with P key
        elif event.type == pygame.KEYDOWN:
            if event.key == pause_key:
                paused = not paused

        # Show "Paused" message when paused
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    paused = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pause_key:
                        paused = not paused

            # display a message "Paused"
            # font = pygame.font.Font(None, 30)
            text = font.render("Paused", True, (0, 0, 0))
            screen.blit(text, (size[0] // 2, size[1] // 2 - 100))
            pygame.display.update()

        # TODO: dont print ESC key stokes for pausing game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                result = check_input(input_text, current_word)
                print(f"Inputted: {input_text}")
                input_text = ""
                if result:
                    print("Correct")
                    correct_words += 1
                    current_word = pick_next_word()
                    if not current_word:
                        dictionary_end = True
                else:
                    print("False")
                    wrong_words += 1
            elif event.key == pygame.K_BACKSPACE:
                # Handle backspace
                input_text = input_text[:-1]
            else:
                # if event.unicode.isalnum() or event.unicode == " ":
                # Add alphanumeric characters and spaces to the input text
                input_text += event.unicode
            green_index = matching_part(input_text, current_word)

    if dictionary_end:
        print(f"Finish")
        pygame.quit()
        sys.exit()

    # Clear the screen
    screen.fill((255, 255, 255))

    # TODO: Fix currect word text colliding with the current word when the word is long
    # Display current word to type
    text_surface1 = font.render("Current word: ", True, (0, 0, 120))
    text_surface2 = font.render(current_word, True, (0, 0, 0))
    # # Position the rectangle in the center of the screen
    text_rect1 = text_surface1.get_rect()
    text_rect2 = text_surface2.get_rect()
    text_rect1.center = (size_x // 2 - 700, size_y // 2)
    text_rect2.center = (size_x // 2 - 700 + text_surface1.get_width(), size_y // 2)
    # # Blit the text surface on the screen
    screen.blit(text_surface1, text_rect1)
    screen.blit(text_surface2, text_rect2)

    # Display all remaining words
    if len(dictionary) > 0:
        text_surface1 = font.render("Remaining: ", True, (0, 0, 255))
        text_surface2 = font.render(remaining_words_readable, True, (0, 0, 0))
        # # Position the rectangle in the center of the screen
        text_rect1 = (size_x // 2 - 800, size_y // 2 - 100)
        text_rect2 = (size_x // 2 - 800 + text_surface1.get_width(), size_y // 2 - 100)
        # # Blit the text surface on the screen
        screen.blit(text_surface1, text_rect1)
        screen.blit(text_surface2, text_rect2)

    # Render the user input text
    text_surface1 = font.render(input_text[:green_index], True, green_color)
    text_surface2 = font.render(input_text[green_index:], True, red_color)
    # # Position the rectangle in the center of the screen
    text_rect1 = (size_x // 2 - 100, size_y // 2 + 100)
    text_rect2 = (size_x // 2 - 100 + text_surface1.get_width(), size_y // 2 + 100)
    # # Blit the text surface on the screen
    screen.blit(text_surface1, text_rect1)
    screen.blit(text_surface2, text_rect2)

    # Display correct words score
    text_surface = font.render("Correct words: " + str(correct_words), True, green_color)
    # Get the rectangle of the text surface
    text_rect = text_surface.get_rect()
    # Position the rectangle in the center of the screen
    text_rect.center = (size_x // 2, size_y // 2 - 200)
    # Blit the text surface on the screen
    screen.blit(text_surface, text_rect)

    # Display wrong words score
    text_surface = font.render("Wrong words: " + str(wrong_words), True, red_color)
    # Get the rectangle of the text surface
    text_rect = text_surface.get_rect()
    # Position the rectangle in the center of the screen
    text_rect.center = (size_x // 2, size_y // 2 - 150)
    # Blit the text surface on the screen
    screen.blit(text_surface, text_rect)

    if endless_game:
        # Draw timer
        text = font.render("Timer: " + str(int((time.time() - start_time))), True, (0, 0, 0))
        screen.blit(text, (size[0] - 200, 10))
    else:
        # Draw the countdown timer
        remaining_time = game_time - (time.time() - start_time)
        text = font.render("Time remaining: " + str(int(remaining_time)), True, (0, 0, 0))
        screen.blit(text, (size[0] - 200, 10))

        # check if game time is up
        if time.time() - start_time > game_time:
            running = False

    # Update the display
    pygame.display.update()
