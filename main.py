import pygame
import os
import msvcrt
import time
import random
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
    print("No music files found.")
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

# Original library
songs = songs.copy()

# Current playback order
play_order = songs.copy()

current_song = 0

paused = False
running = True

loop = False
shuffle = False

song_duration = 0

last_status_update = 0

display_started = False


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

    if seconds < 0:
        seconds = 0

    minutes = seconds // 60
    seconds = seconds % 60

    return f"{minutes:02}:{seconds:02}"


# ==========================================
# 8. UPDATE ECHO POD DISPLAY
# ==========================================

def update_display():

    global last_status_update
    global display_started

    position = pygame.mixer.music.get_pos() // 1000

    if position < 0:
        position = 0

    filename = play_order[current_song]

    # --------------------------------------
    # LOOP / SHUFFLE ICONS
    # --------------------------------------

    icons = ""

    if loop:
        icons += "🔁 LOOP   "

    if shuffle:
        icons += "🔀 SHUFFLE"

    # --------------------------------------
    # PLAYBACK STATE
    # --------------------------------------

    if paused:
        playback_state = "PAUSED"
    else:
        playback_state = "PLAYING"

    # --------------------------------------
    # MOVE CURSOR BACK TO DISPLAY
    # --------------------------------------

    if display_started:

        # Move up 4 lines
        print("\033[4A", end="")

    # --------------------------------------
    # PRINT THE 4 DISPLAY LINES
    # --------------------------------------

    print(
        f"\r\033[K{icons}"
    )

    print(
        f"\r\033[K{playback_state}"
    )

    print(
        f"\r\033[K{filename}"
    )

    print(
        f"\r\033[K{format_time(position)} / "
        f"{format_time(song_duration)}"
    )

    display_started = True

    last_status_update = time.time()


# ==========================================
# 9. PLAY SONG
# ==========================================

def play_song():

    global song_duration
    global paused
    global last_status_update

    filename = play_order[current_song]

    path = os.path.join(music_folder, filename)

    try:

        # Clear old song-finished events
        pygame.event.clear(SONG_FINISHED)

        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

        paused = False

        song_duration = get_song_duration(filename)

        last_status_update = 0

        return True

    except pygame.error:

        return False


# ==========================================
# 10. NEXT SONG
# ==========================================

def next_song():

    global current_song
    global running

    if current_song < len(play_order) - 1:

        current_song += 1

        if play_song():
            update_display()

    else:

        if loop:

            current_song = 0

            if play_song():
                update_display()

        else:

            pygame.mixer.music.stop()

            running = False


# ==========================================
# 11. PREVIOUS SONG
# ==========================================

def previous_song():

    global current_song

    if current_song > 0:

        current_song -= 1

    else:

        if loop:
            current_song = len(play_order) - 1
        else:
            current_song = 0

    if play_song():
        update_display()


# ==========================================
# 12. PAUSE / RESUME
# ==========================================

def toggle_pause():

    global paused

    if paused:

        pygame.mixer.music.unpause()
        paused = False

    else:

        pygame.mixer.music.pause()
        paused = True

    update_display()


# ==========================================
# 13. TOGGLE LOOP
# ==========================================

def toggle_loop():

    global loop

    loop = not loop

    update_display()


# ==========================================
# 14. TOGGLE SHUFFLE
# ==========================================

def toggle_shuffle():

    global shuffle
    global play_order
    global current_song

    # Remember current song
    current_filename = play_order[current_song]

    # --------------------------------------
    # SHUFFLE ON
    # --------------------------------------

    if not shuffle:

        shuffle = True

        play_order = songs.copy()

        random.shuffle(play_order)

        # Keep current song first
        play_order.remove(current_filename)
        play_order.insert(0, current_filename)

        current_song = 0

    # --------------------------------------
    # SHUFFLE OFF
    # --------------------------------------

    else:

        shuffle = False

        play_order = songs.copy()

        current_song = play_order.index(current_filename)

    update_display()


# ==========================================
# 15. KEYBOARD INPUT
# ==========================================

def get_command():

    if not msvcrt.kbhit():
        return None

    key = msvcrt.getch()

    if key in (b'n', b'N'):
        return "next"

    elif key in (b'p', b'P'):
        return "previous"

    elif key == b' ':
        return "pause"

    elif key in (b'l', b'L'):
        return "loop"

    elif key in (b's', b'S'):
        return "shuffle"

    elif key == b'\x1b':
        return "exit"

    return None


# ==========================================
# 16. START FIRST SONG
# ==========================================

if not play_song():

    pygame.mixer.quit()
    pygame.quit()

    input("Press ENTER to exit...")
    exit()


# ==========================================
# 17. CONTROLS
# ==========================================

print("================================")
print("          ECHO POD M3")
print("================================")
print("N     = Next")
print("P     = Previous")
print("SPACE = Pause / Resume")
print("L     = Loop ON / OFF")
print("S     = Shuffle ON / OFF")
print("ESC   = Exit")
print("================================")
print()


# ==========================================
# 18. INITIAL DISPLAY
# ==========================================

update_display()


# ==========================================
# 19. MAIN LOOP
# ==========================================

while running:

    # --------------------------------------
    # KEYBOARD
    # --------------------------------------

    command = get_command()

    if command == "next":

        next_song()

    elif command == "previous":

        previous_song()

    elif command == "pause":

        toggle_pause()

    elif command == "loop":

        toggle_loop()

    elif command == "shuffle":

        toggle_shuffle()

    elif command == "exit":

        pygame.event.clear(SONG_FINISHED)

        pygame.mixer.music.stop()

        running = False

        break


    # --------------------------------------
    # SONG FINISHED
    # --------------------------------------

    for event in pygame.event.get():

        if event.type == SONG_FINISHED:

            if running and not paused:

                next_song()


    # --------------------------------------
    # TIMER UPDATE
    # --------------------------------------

    if running:

        current_time = time.time()

        if current_time - last_status_update >= 1:

            update_display()


    time.sleep(0.01)


# ==========================================
# 20. CLEAN UP
# ==========================================

pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()

print()
print("Echo Pod stopped.")