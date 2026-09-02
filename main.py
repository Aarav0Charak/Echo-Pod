import pygame
import os
import msvcrt
import time


# ==========================================
# 1. FIND SONGS
# ==========================================

music_folder = "music"
supported_formats = (".mp3", ".wav", ".ogg")

songs = []

for file in os.listdir(music_folder):
    if file.lower().endswith(supported_formats):
        songs.append(file)

songs.sort()


# ==========================================
# 2. CHECK FOR EMPTY MUSIC FOLDER
# ==========================================

if len(songs) == 0:
    print("No supported music files found in the music folder.")
    input("Press ENTER to exit...")
    exit()


# ==========================================
# 3. INITIALIZE PYGAME AUDIO
# ==========================================

pygame.init()
pygame.mixer.init()


# ==========================================
# 4. CREATE SONG-FINISHED EVENT
# ==========================================

SONG_FINISHED = pygame.USEREVENT + 1

pygame.mixer.music.set_endevent(SONG_FINISHED)


# ==========================================
# 5. CURRENT SONG
# ==========================================

current_song = 0
paused = False
running = True


# ==========================================
# 6. PLAY SONG FUNCTION
# ==========================================

def play_song(index):

    song_path = os.path.join(
        music_folder,
        songs[index]
    )

    try:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()

        print("Now playing:", songs[index])

        return True

    except pygame.error as error:
        print("Could not play:", songs[index])
        print("Error:", error)

        return False


# ==========================================
# 7. START FIRST SONG
# ==========================================

if not play_song(current_song):

    pygame.mixer.quit()
    pygame.quit()

    input("Press ENTER to exit...")
    exit()


# ==========================================
# 8. SHOW CONTROLS
# ==========================================

print()
print("==============================")
print("         ECHO POD M2")
print("==============================")
print("N     = Next song")
print("P     = Previous song")
print("SPACE = Pause / Resume")
print("ESC   = Stop and Exit")
print("==============================")
print()


# ==========================================
# 9. MAIN LOOP
# ==========================================

while running:

    # --------------------------------------
    # CHECK KEYBOARD
    # --------------------------------------

    if msvcrt.kbhit():

        key = msvcrt.getch()


        # NEXT
        if key in (b'n', b'N'):

            current_song = (current_song + 1) % len(songs)

            play_song(current_song)

            paused = False


        # PREVIOUS
        elif key in (b'p', b'P'):

            current_song = (current_song - 1) % len(songs)

            play_song(current_song)

            paused = False


        # SPACE
        elif key == b' ':

            if paused:

                pygame.mixer.music.unpause()
                paused = False

                print("Resumed")

            else:

                pygame.mixer.music.pause()
                paused = True

                print("Paused")


        # ESC
        elif key == b'\x1b':

            pygame.mixer.music.stop()
            running = False


    # --------------------------------------
    # CHECK PYGAME EVENTS
    # --------------------------------------

    for event in pygame.event.get():

        if event.type == SONG_FINISHED:

            current_song = (current_song + 1) % len(songs)

            play_song(current_song)

            paused = False


    # Prevent excessive CPU usage
    time.sleep(0.01)


# ==========================================
# 10. CLEAN UP
# ==========================================

pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()

print("Echo Pod stopped.")