import pygame
import os
import msvcrt
import time
from mutagen import File


# ==========================================
# 1. MUSIC LIBRARY
# ==========================================

music_folder = "music"
supported_formats = (".mp3", ".wav", ".ogg")

songs = []

for file in os.listdir(music_folder):

    if file.lower().endswith(supported_formats):
        songs.append(file)

songs.sort()


# ==========================================
# 2. CHECK MUSIC FOLDER
# ==========================================

if len(songs) == 0:

    print("No music files found in the music folder.")
    input("Press ENTER to exit...")
    exit()


# ==========================================
# 3. INITIALIZE PYGAME
# ==========================================

pygame.init()
pygame.mixer.init()


# ==========================================
# 4. SONG FINISHED EVENT
# ==========================================

SONG_FINISHED = pygame.USEREVENT + 1

pygame.mixer.music.set_endevent(SONG_FINISHED)


# ==========================================
# 5. PLAYER STATE
# ==========================================

current_song = 0
paused = False
running = True

song_duration = 0

last_status_update = 0
status_was_paused = False


# ==========================================
# 6. GET SONG DURATION
# ==========================================

def get_song_duration(filename):

    path = os.path.join(music_folder, filename)

    try:

        audio = File(path)

        if audio is not None:
            return int(audio.info.length)

    except Exception:
        pass

    return 0


# ==========================================
# 7. FORMAT TIME
# ==========================================

def format_time(seconds):

    minutes = seconds // 60
    seconds = seconds % 60

    return f"{minutes:02}:{seconds:02}"


# ==========================================
# 8. PLAY CURRENT SONG
# ==========================================

def play_current_song():

    global song_duration
    global paused
    global status_was_paused
    global last_status_update

    song_path = os.path.join(
        music_folder,
        songs[current_song]
    )

    try:

        pygame.event.clear(SONG_FINISHED)

        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()

        paused = False

        song_duration = get_song_duration(
            songs[current_song]
        )

        status_was_paused = False
        last_status_update = 0

        print()
        print("Now playing:", songs[current_song])

        return True

    except pygame.error as error:

        print("Could not play:", songs[current_song])
        print("Error:", error)

        return False


# ==========================================
# 9. NEXT SONG
# ==========================================

def next_song():

    global current_song

    current_song = (current_song + 1) % len(songs)

    play_current_song()


# ==========================================
# 10. PREVIOUS SONG
# ==========================================

def previous_song():

    global current_song

    current_song = (current_song - 1) % len(songs)

    play_current_song()


# ==========================================
# 11. PAUSE / RESUME
# ==========================================

def toggle_pause():

    global paused
    global status_was_paused

    if paused:

        pygame.mixer.music.unpause()

        paused = False
        status_was_paused = False

    else:

        pygame.mixer.music.pause()

        paused = True
        status_was_paused = False


# ==========================================
# 12. GET KEYBOARD COMMAND
# ==========================================

def get_command():

    if not msvcrt.kbhit():
        return None

    key = msvcrt.getch()

    if key in (b'n', b'N'):
        return "next"

    if key in (b'p', b'P'):
        return "previous"

    if key == b' ':
        return "pause"

    if key == b'\x1b':
        return "exit"

    return None


# ==========================================
# 13. START FIRST SONG
# ==========================================

if not play_current_song():

    pygame.mixer.quit()
    pygame.quit()

    input("Press ENTER to exit...")
    exit()


# ==========================================
# 14. DISPLAY CONTROLS
# ==========================================

print()
print("================================")
print("          ECHO POD M3")
print("================================")
print("N     = Next")
print("P     = Previous")
print("SPACE = Pause / Resume")
print("ESC   = Exit")
print("================================")
print()


# ==========================================
# 15. MAIN LOOP
# ==========================================

while running:

    # --------------------------------------
    # Keyboard input
    # --------------------------------------

    command = get_command()


    if command == "next":

        next_song()


    elif command == "previous":

        previous_song()


    elif command == "pause":

        toggle_pause()


    elif command == "exit":

        pygame.mixer.music.stop()
        running = False


    # --------------------------------------
    # Song finished naturally
    # --------------------------------------

    for event in pygame.event.get():

        if event.type == SONG_FINISHED:

            next_song()


    # --------------------------------------
    # Update timer
    # --------------------------------------

    current_time = time.time()

    if paused:

        if not status_was_paused:

            position = pygame.mixer.music.get_pos() // 1000

            print(
                f"\rPAUSED  | {format_time(position)} / "
                f"{format_time(song_duration)}",
                end="",
                flush=True
            )

            status_was_paused = True

    else:

        status_was_paused = False

        if current_time - last_status_update >= 1:

            position = pygame.mixer.music.get_pos() // 1000

            print(
                f"\rPLAYING | {format_time(position)} / "
                f"{format_time(song_duration)}",
                end="",
                flush=True
            )

            last_status_update = current_time


    # Small delay
    time.sleep(0.01)


# ==========================================
# 16. CLEAN UP
# ==========================================

pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()

print()
print("Echo Pod stopped.")