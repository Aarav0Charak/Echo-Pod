import pygame
import os
import msvcrt
import time

# -----------------------------
# 1. Set up the music file path
# -----------------------------

music_file = os.path.join("music", "test.mp3")

# Check if the file exists
if not os.path.exists(music_file):
    print("Error: test.mp3 was not found in the music folder.")
    input("Press ENTER to exit...")
    exit()


# -----------------------------
# 2. Initialize pygame audio
# -----------------------------

pygame.mixer.init()


# -----------------------------
# 3. Load the song
# -----------------------------

try:
    pygame.mixer.music.load(music_file)

except pygame.error:
    print("Error: pygame could not load test.mp3.")
    input("Press ENTER to exit...")
    pygame.mixer.quit()
    exit()


# -----------------------------
# 4. Start playing
# -----------------------------

pygame.mixer.music.play()

print("Now playing: test.mp3")
print()
print("SPACE = Pause / Resume")
print("ESC   = Stop and Exit")


# -----------------------------
# 5. Keep the program running
# -----------------------------

running = True
paused = False

while running:

    # Check if a key has been pressed
    if msvcrt.kbhit():

        key = msvcrt.getch()

        # ESC key
        if key == b'\x1b':
            pygame.mixer.music.stop()
            running = False

        # SPACE key
        elif key == b' ':

            if paused:
                pygame.mixer.music.unpause()
                paused = False
                print("Resumed")

            else:
                pygame.mixer.music.pause()
                paused = True
                print("Paused")

    # Stop when the song finishes naturally
    if not paused and not pygame.mixer.music.get_busy():
        running = False

    # Small delay so the loop doesn't use 100% CPU
    time.sleep(0.01)


# -----------------------------
# 6. Clean up
# -----------------------------

pygame.mixer.quit()

print("Echo Pod stopped.")