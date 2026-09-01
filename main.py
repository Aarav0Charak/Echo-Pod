from pathlib import Path

music_file = Path("music/test.mp3")

print("Looking for:", music_file)

if music_file.exists():
    print("Music file found!")
else:
    print("Music file NOT found!")