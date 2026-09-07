import os
from mutagen import File


# ==========================================
# MUSIC FOLDER
# ==========================================

music_folder = "music"
supported_formats = (".mp3", ".wav", ".ogg")


# ==========================================
# FIND SONGS
# ==========================================

songs = []

for file in os.listdir(music_folder):

    if file.lower().endswith(supported_formats):
        songs.append(file)

songs.sort()


# ==========================================
# READ SONG INFORMATION
# ==========================================

for song in songs:

    path = os.path.join(music_folder, song)

    try:

        audio = File(path)

        print("--------------------------------")
        print("File:", song)

        if audio is not None:

            title = audio.get("TIT2")
            artist = audio.get("TPE1")
            album = audio.get("TALB")

            if title:
                print("Title:", title[0])
            else:
                print("Title: Unknown")

            if artist:
                print("Artist:", artist[0])
            else:
                print("Artist: Unknown")

            if album:
                print("Album:", album[0])
            else:
                print("Album: Unknown")

        else:

            print("Could not read song information.")

    except Exception as error:

        print("Error reading:", song)
        print(error)