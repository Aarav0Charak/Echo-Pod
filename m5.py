import tkinter as tk
import pygame
import os
import random
import math
import time

from PIL import Image, ImageTk, ImageFilter


# ============================================================
# ECHO POD
# CYBERPUNK NIGHTCORE MUSIC PLAYER
# ============================================================

MUSIC_FOLDER = "music"
SUPPORTED_FORMATS = (".mp3", ".wav", ".ogg")

ALBUM_ART_PATH = os.path.join("assets", "cover.png")

WIDTH = 600
HEIGHT = 720

BG = "#030205"

PINK = "#ff1760"
PINK2 = "#ff3d78"
PINK_DARK = "#65102d"

WHITE = "#f7edf1"
GREY = "#806f77"

BLACK = "#050306"


# ============================================================
# MUSIC
# ============================================================

songs = [
    file
    for file in os.listdir(MUSIC_FOLDER)
    if file.lower().endswith(SUPPORTED_FORMATS)
]

songs.sort()

if not songs:
    print("No songs found in music/")
    raise SystemExit


# ============================================================
# PYGAME
# ============================================================

pygame.init()

pygame.display.set_mode(
    (1, 1),
    pygame.HIDDEN
)

pygame.mixer.init()

SONG_FINISHED = pygame.USEREVENT + 1

pygame.mixer.music.set_endevent(
    SONG_FINISHED
)


# ============================================================
# PLAYER STATE
# ============================================================

play_order = songs.copy()

current_song = 0

paused = False
loop = False
shuffle = False

running = True

song_duration = 0


# ============================================================
# WINDOW
# ============================================================

window = tk.Tk()

window.title("ECHO POD")

# Center the window on the actual screen instead of letting
# the OS drop it at a default top-left-ish spot — on a short
# screen that default position is exactly what pushed the
# bottom of the player off-screen before.

window.update_idletasks()

_screen_w = window.winfo_screenwidth()
_screen_h = window.winfo_screenheight()

_pos_x = max(0, (_screen_w - WIDTH) // 2)
_pos_y = max(20, (_screen_h - HEIGHT) // 2 - 20)

window.geometry(
    f"{WIDTH}x{HEIGHT}+{_pos_x}+{_pos_y}"
)

window.configure(
    bg=BG
)

window.resizable(
    False,
    False
)


# ============================================================
# CANVAS
# ============================================================

canvas = tk.Canvas(
    window,
    width=WIDTH,
    height=HEIGHT,
    bg=BG,
    highlightthickness=0
)

canvas.pack()


# ============================================================
# BACKGROUND
# ============================================================

for y in range(HEIGHT):

    ratio = y / HEIGHT

    r = int(3 + ratio * 4)
    g = int(2 + ratio)
    b = int(5 + ratio * 6)

    canvas.create_line(
        0,
        y,
        WIDTH,
        y,
        fill=f"#{r:02x}{g:02x}{b:02x}"
    )


# ============================================================
# CITY BACKGROUND
# ============================================================

# Far buildings

random.seed(21)

for x in range(
    0,
    WIDTH,
    32
):

    building_height = random.randint(
        180,
        430
    )

    top = HEIGHT - building_height

    canvas.create_rectangle(
        x,
        top,
        x + random.randint(22, 38),
        HEIGHT,
        fill=random.choice([
            "#070509",
            "#09050a",
            "#0b060c"
        ]),
        outline="#170914"
    )


# Building windows

for _ in range(160):

    x = random.randint(
        5,
        WIDTH - 8
    )

    y = random.randint(
        150,
        HEIGHT - 100
    )

    if random.random() < 0.6:

        canvas.create_rectangle(
            x,
            y,
            x + random.randint(2, 5),
            y + random.randint(2, 7),
            fill=random.choice([
                "#260b18",
                "#401025",
                "#68132d"
            ]),
            outline=""
        )


# ============================================================
# NEON CITY LINES
# ============================================================

for i in range(6):

    y = 250 + i * 65

    canvas.create_line(
        0,
        y,
        WIDTH,
        y,
        fill="#160912",
        width=1
    )


# ============================================================
# RAIN
# ============================================================

rain = []

for _ in range(100):

    x = random.randint(
        0,
        WIDTH
    )

    y = random.randint(
        0,
        HEIGHT
    )

    speed = random.uniform(
        0.8,
        2.8
    )

    length = random.randint(
        5,
        18
    )

    item = canvas.create_line(
        x,
        y,
        x - 2,
        y + length,
        fill=random.choice([
            "#160912",
            "#21101a",
            "#321021",
            "#531027"
        ]),
        width=1
    )

    rain.append({
        "item": item,
        "x": x,
        "y": y,
        "speed": speed,
        "length": length
    })


def animate_rain():

    if not running:
        return

    for drop in rain:

        drop["y"] += drop["speed"]

        if drop["y"] > HEIGHT:

            drop["y"] = random.randint(
                -50,
                -5
            )

            drop["x"] = random.randint(
                0,
                WIDTH
            )

        canvas.coords(
            drop["item"],
            drop["x"],
            drop["y"],
            drop["x"] - 2,
            drop["y"] + drop["length"]
        )

    window.after(
        25,
        animate_rain
    )


# ============================================================
# NEON BORDER
# ============================================================

canvas.create_rectangle(
    14,
    14,
    WIDTH - 14,
    HEIGHT - 14,
    outline="#3b0e20",
    width=1
)

canvas.create_rectangle(
    18,
    18,
    WIDTH - 18,
    HEIGHT - 18,
    outline="#a71948",
    width=1
)


# Top-left corner

canvas.create_line(
    18,
    18,
    62,
    18,
    fill=PINK,
    width=4
)

canvas.create_line(
    18,
    18,
    18,
    62,
    fill=PINK,
    width=4
)


# Top-right

canvas.create_line(
    WIDTH - 62,
    18,
    WIDTH - 18,
    18,
    fill=PINK,
    width=4
)

canvas.create_line(
    WIDTH - 18,
    18,
    WIDTH - 18,
    62,
    fill=PINK,
    width=4
)


# Bottom corners

canvas.create_line(
    18,
    HEIGHT - 18,
    62,
    HEIGHT - 18,
    fill=PINK,
    width=4
)

canvas.create_line(
    18,
    HEIGHT - 62,
    18,
    HEIGHT - 18,
    fill=PINK,
    width=4
)

canvas.create_line(
    WIDTH - 62,
    HEIGHT - 18,
    WIDTH - 18,
    HEIGHT - 18,
    fill=PINK,
    width=4
)

canvas.create_line(
    WIDTH - 18,
    HEIGHT - 62,
    WIDTH - 18,
    HEIGHT - 18,
    fill=PINK,
    width=4
)


# ============================================================
# HEADER
# ============================================================

canvas.create_text(
    42,
    52,
    text="ECHO",
    anchor="w",
    fill=WHITE,
    font=("Arial", 28, "bold")
)

canvas.create_text(
    150,
    52,
    text="POD",
    anchor="w",
    fill=PINK,
    font=("Arial", 28, "bold")
)

canvas.create_text(
    44,
    82,
    text="M U S I C   L I V E S   L O N G E R",
    anchor="w",
    fill="#796a71",
    font=("Arial", 8)
)


# Note: no custom minimize/maximize/close icons are drawn
# here anymore — the real OS titlebar already has them, and
# drawing a second set just duplicated them on screen.


# ============================================================
# SIDE MARGIN TEXT (LEFT)
# ============================================================
# Mirrors the vertical kanji + "NIGHT DRIVE" strip that runs
# down the left edge of the reference artwork.

canvas.create_line(
    30,
    160,
    46,
    160,
    fill=PINK,
    width=2
)

canvas.create_text(
    38,
    230,
    text="夜\n行",
    anchor="n",
    justify="center",
    fill=PINK,
    font=("Arial", 22, "bold")
)

canvas.create_text(
    38,
    330,
    text="N\nI\nG\nH\nT\n\nD\nR\nI\nV\nE",
    anchor="n",
    justify="center",
    fill="#6b5860",
    font=("Arial", 9, "bold")
)


# ============================================================
# SIDE MARGIN TEXT (RIGHT)
# ============================================================
# Mirrors the vertical Japanese phrase running down the
# right edge of the reference artwork.

canvas.create_text(
    562,
    160,
    text="音\n楽\nで\n、\nま\nだ\nど\nこ\nか\nへ\n—",
    anchor="n",
    justify="center",
    fill="#9c6b78",
    font=("Arial", 13)
)


# ============================================================
# ALBUM COVER
# ============================================================

ART_SIZE = 300

ART_X = 150
ART_Y = 95


# ============================================================
# ALBUM ART (LOADED FROM THE USER'S ARTWORK)
# ============================================================

def load_album_cover():

    try:

        img = Image.open(
            ALBUM_ART_PATH
        ).convert("RGB")

        # The source picture is the full reference mockup
        # (whole app screenshot), so crop out just the square
        # album-art illustration in the middle of it. Both
        # axes use the same scale (w/600 == h/900, since the
        # mockup and the app canvas share a 2:3 aspect ratio),
        # then a small inward pad drops the mockup's own frame
        # border/text sliver at the crop's edge.

        w, h = img.size

        scale = w / 600

        pad = 14

        left = int(ART_X * scale) + pad
        top = int(ART_Y * scale) + pad
        right = int((ART_X + ART_SIZE) * scale) - pad
        bottom = int((ART_Y + ART_SIZE) * scale) - pad

        img = img.crop(
            (
                left,
                top,
                right,
                bottom
            )
        )

        img = img.resize(
            (
                ART_SIZE,
                ART_SIZE
            ),
            Image.LANCZOS
        )

        # Subtle neon glow, matching the rest of the UI

        glow = img.filter(
            ImageFilter.GaussianBlur(2)
        )

        img = Image.blend(
            img,
            glow,
            0.12
        )

    except Exception as error:

        print(
            "Could not load album art:",
            error
        )

        img = Image.new(
            "RGB",
            (ART_SIZE, ART_SIZE),
            "#150910"
        )

    return ImageTk.PhotoImage(
        img
    )


# ============================================================
# DISPLAY ALBUM COVER
# ============================================================

album_cover = load_album_cover()

album_label = tk.Label(
    window,
    image=album_cover,
    bg="#050306",
    borderwidth=0
)

album_label.place(
    x=ART_X,
    y=ART_Y
)

album_label.image = album_cover


# Note: the cover used to gently float via a repeating
# window.after() reposition loop, which is the "keeps
# moving" jitter — removed so the artwork just sits still.


# ============================================================
# COVER FRAME
# ============================================================

canvas.create_rectangle(
    ART_X - 5,
    ART_Y - 5,
    ART_X + ART_SIZE + 5,
    ART_Y + ART_SIZE + 5,
    outline="#350d1d",
    width=2
)

canvas.create_rectangle(
    ART_X - 2,
    ART_Y - 2,
    ART_X + ART_SIZE + 2,
    ART_Y + ART_SIZE + 2,
    outline=PINK,
    width=2
)


# ============================================================
# NOW PLAYING
# ============================================================

canvas.create_text(
    150,
    408,
    text="NOW PLAYING",
    anchor="w",
    fill=PINK,
    font=("Arial", 9, "bold")
)


title_label = tk.Label(
    window,
    text="",
    bg=BG,
    fg=WHITE,
    anchor="w",
    font=("Arial", 25, "bold")
)

title_label.place(
    x=150,
    y=416,
    width=335,
    height=32
)


artist_label = tk.Label(
    window,
    text="",
    bg=BG,
    fg="#89777f",
    anchor="w",
    font=("Arial", 13)
)

artist_label.place(
    x=150,
    y=450,
    width=335,
    height=22
)


# ============================================================
# FAVORITE HEART
# ============================================================

heart = canvas.create_text(
    515,
    430,
    text="♡",
    fill=PINK,
    font=("Arial", 32)
)


def toggle_favorite(event=None):

    current = canvas.itemcget(
        heart,
        "text"
    )

    if current == "♡":

        canvas.itemconfig(
            heart,
            text="♥",
            fill=PINK
        )

    else:

        canvas.itemconfig(
            heart,
            text="♡",
            fill=PINK
        )


canvas.tag_bind(
    heart,
    "<Button-1>",
    toggle_favorite
)


# ============================================================
# PROGRESS
# ============================================================

PROGRESS_LEFT = 150
PROGRESS_RIGHT = 495
PROGRESS_Y = 485


canvas.create_line(
    PROGRESS_LEFT,
    PROGRESS_Y,
    PROGRESS_RIGHT,
    PROGRESS_Y,
    fill="#34232b",
    width=6
)


progress = canvas.create_line(
    PROGRESS_LEFT,
    PROGRESS_Y,
    PROGRESS_LEFT,
    PROGRESS_Y,
    fill=PINK,
    width=6
)


progress_dot = canvas.create_oval(
    PROGRESS_LEFT - 6,
    PROGRESS_Y - 6,
    PROGRESS_LEFT + 6,
    PROGRESS_Y + 6,
    fill=PINK2,
    outline=""
)


current_time = tk.Label(
    window,
    text="00:00",
    bg=BG,
    fg=PINK,
    font=("Arial", 9, "bold")
)

current_time.place(
    x=150,
    y=497,
    width=60,
    height=20
)


total_time = tk.Label(
    window,
    text="00:00",
    bg=BG,
    fg=PINK,
    font=("Arial", 9, "bold")
)

total_time.place(
    x=440,
    y=497,
    width=55,
    height=20
)


# ============================================================
# TIME
# ============================================================

def format_time(seconds):

    seconds = max(
        0,
        int(seconds)
    )

    return (
        f"{seconds // 60:02d}:"
        f"{seconds % 60:02d}"
    )


# ============================================================
# METADATA
# ============================================================

song_overrides = {
    "Loving Machine - TV Girl.mp3": {
        "title": "Loving Machine",
        "artist": "TV Girl"
    },

    "Frank Ocean - American Wedding (Lyrics).mp3": {
        "title": "American Wedding",
        "artist": "Frank Ocean"
    }
}


def get_song_info(filename):

    path = os.path.join(
        MUSIC_FOLDER,
        filename
    )

    title = None
    artist = None
    duration = 0


    if filename in song_overrides:

        title = song_overrides[
            filename
        ]["title"]

        artist = song_overrides[
            filename
        ]["artist"]


    try:

        from mutagen import File

        audio = File(
            path,
            easy=True
        )

        if audio:

            if not title:

                value = audio.get(
                    "title"
                )

                if value:
                    title = value[0]


            if not artist:

                value = audio.get(
                    "artist"
                )

                if value:
                    artist = value[0]


            if audio.info:

                duration = int(
                    audio.info.length
                )

    except Exception:
        pass


    if not title:

        title = os.path.splitext(
            filename
        )[0]


    if not artist:

        artist = "Unknown Artist"


    return (
        title,
        artist,
        duration
    )


# ============================================================
# TITLE FONT
# ============================================================

def title_font(title):

    length = len(title)

    if length <= 22:

        return (
            "Arial",
            22,
            "bold"
        )

    if length <= 32:

        return (
            "Arial",
            18,
            "bold"
        )

    if length <= 42:

        return (
            "Arial",
            15,
            "bold"
        )

    return (
        "Arial",
        13,
        "bold"
    )


# ============================================================
# UPDATE SONG DISPLAY
# ============================================================

def update_song_display():

    filename = play_order[
        current_song
    ]

    title, artist, duration = (
        get_song_info(filename)
    )

    global song_duration

    song_duration = duration


    title_label.config(
        text=title,
        font=title_font(title)
    )

    artist_label.config(
        text=artist
    )

    current_time.config(
        text="00:00"
    )

    total_time.config(
        text=format_time(duration)
    )


    canvas.coords(
        progress,
        PROGRESS_LEFT,
        PROGRESS_Y,
        PROGRESS_LEFT,
        PROGRESS_Y
    )

    canvas.coords(
        progress_dot,
        PROGRESS_LEFT - 6,
        PROGRESS_Y - 6,
        PROGRESS_LEFT + 6,
        PROGRESS_Y + 6
    )


# ============================================================
# PLAY SONG
# ============================================================

def play_song():

    global paused

    filename = play_order[
        current_song
    ]

    path = os.path.join(
        MUSIC_FOLDER,
        filename
    )


    try:

        pygame.event.clear(
            SONG_FINISHED
        )

        pygame.mixer.music.load(
            path
        )

        pygame.mixer.music.play()

        paused = False

        update_song_display()

        update_play_button()

    except Exception as error:

        print(
            "Could not play:",
            filename
        )

        print(error)


# ============================================================
# NEXT
# ============================================================

def next_song():

    global current_song

    current_song += 1


    if current_song >= len(
        play_order
    ):

        current_song = 0


    play_song()


# ============================================================
# PREVIOUS
# ============================================================

def previous_song():

    global current_song

    current_song -= 1


    if current_song < 0:

        current_song = (
            len(play_order) - 1
        )


    play_song()


# ============================================================
# PAUSE
# ============================================================

def toggle_pause():

    global paused

    if paused:

        pygame.mixer.music.unpause()

        paused = False

    else:

        pygame.mixer.music.pause()

        paused = True


    update_play_button()


# ============================================================
# MAIN PLAY BUTTON
# ============================================================

play_outer = canvas.create_oval(
    252,
    517,
    348,
    613,
    outline="#431126",
    width=2
)


play_circle = canvas.create_oval(
    262,
    527,
    338,
    603,
    fill="#070507",
    outline=PINK,
    width=3
)


play_symbol = canvas.create_text(
    300,
    565,
    text="Ⅱ",
    fill=WHITE,
    font=("Arial", 28, "bold")
)


def update_play_button():

    if paused:

        canvas.itemconfig(
            play_symbol,
            text="▶"
        )

    else:

        canvas.itemconfig(
            play_symbol,
            text="Ⅱ"
        )


def click_play(event=None):

    canvas.itemconfig(
        play_circle,
        outline=WHITE
    )

    window.after(
        120,
        lambda: canvas.itemconfig(
            play_circle,
            outline=PINK
        )
    )

    toggle_pause()


canvas.tag_bind(
    play_circle,
    "<Button-1>",
    click_play
)

canvas.tag_bind(
    play_symbol,
    "<Button-1>",
    click_play
)


# ============================================================
# CONTROL BUTTON
# ============================================================

def control_button(
    x,
    y,
    symbol,
    command
):

    outer = canvas.create_oval(
        x - 30,
        y - 30,
        x + 30,
        y + 30,
        outline="#271923",
        width=1
    )

    ring = canvas.create_oval(
        x - 24,
        y - 24,
        x + 24,
        y + 24,
        outline="#68122f",
        width=2
    )

    text = canvas.create_text(
        x,
        y,
        text=symbol,
        fill=WHITE,
        font=("Arial", 19, "bold")
    )


    def click(event=None):

        canvas.itemconfig(
            ring,
            outline=PINK
        )

        canvas.itemconfig(
            text,
            fill=PINK2
        )

        command()

        window.after(
            150,
            reset
        )


    def reset():

        canvas.itemconfig(
            ring,
            outline="#68122f"
        )

        canvas.itemconfig(
            text,
            fill=WHITE
        )


    canvas.tag_bind(
        outer,
        "<Button-1>",
        click
    )

    canvas.tag_bind(
        ring,
        "<Button-1>",
        click
    )

    canvas.tag_bind(
        text,
        "<Button-1>",
        click
    )

    return ring, text


# ============================================================
# SHUFFLE
# ============================================================

def toggle_shuffle():

    global shuffle
    global play_order
    global current_song

    filename = play_order[
        current_song
    ]

    shuffle = not shuffle


    if shuffle:

        play_order = songs.copy()

        random.shuffle(
            play_order
        )

        play_order.remove(
            filename
        )

        play_order.insert(
            0,
            filename
        )

        current_song = 0

    else:

        play_order = songs.copy()

        current_song = (
            play_order.index(
                filename
            )
        )


    update_shuffle()


# ============================================================
# LOOP
# ============================================================

def toggle_loop():

    global loop

    loop = not loop

    update_loop()


# ============================================================
# CONTROLS
# ============================================================

shuffle_ring, shuffle_text = control_button(
    105,
    565,
    "⇄",
    toggle_shuffle
)


previous_ring, previous_text = control_button(
    195,
    565,
    "◀",
    previous_song
)


next_ring, next_text = control_button(
    405,
    565,
    "▶",
    next_song
)


loop_ring, loop_text = control_button(
    495,
    565,
    "↻",
    toggle_loop
)


# ============================================================
# LABELS
# ============================================================

canvas.create_text(
    105,
    608,
    text="SHUFFLE",
    fill=PINK,
    font=("Arial", 8, "bold")
)

canvas.create_text(
    495,
    608,
    text="LOOP",
    fill=PINK,
    font=("Arial", 8, "bold")
)


# ============================================================
# BUTTON STATES
# ============================================================

def update_shuffle():

    if shuffle:

        canvas.itemconfig(
            shuffle_ring,
            outline=PINK
        )

        canvas.itemconfig(
            shuffle_text,
            fill=PINK
        )

    else:

        canvas.itemconfig(
            shuffle_ring,
            outline="#68122f"
        )

        canvas.itemconfig(
            shuffle_text,
            fill=WHITE
        )


def update_loop():

    if loop:

        canvas.itemconfig(
            loop_ring,
            outline=PINK
        )

        canvas.itemconfig(
            loop_text,
            fill=PINK
        )

    else:

        canvas.itemconfig(
            loop_ring,
            outline="#68122f"
        )

        canvas.itemconfig(
            loop_text,
            fill=WHITE
        )


# ============================================================
# DIGITAL EQUALIZER
# ============================================================

EQ_COUNT = 42

EQ_START = 90

# Keep the bars confined to the strip below the transport
# buttons (which bottom out around y=595) so they never
# grow up into the play/shuffle/loop controls.

EQ_BOTTOM = 648

EQ_MAX_HEIGHT = 18

EQ_WIDTH = 5

EQ_GAP = 5


equalizer = []

for i in range(EQ_COUNT):

    x = (
        EQ_START
        +
        i * (
            EQ_WIDTH
            +
            EQ_GAP
        )
    )

    bar = canvas.create_rectangle(
        x,
        EQ_BOTTOM - 3,
        x + EQ_WIDTH,
        EQ_BOTTOM,
        fill=PINK,
        outline="",
        tags=("eq_bar",)
    )

    equalizer.append({
        "id": bar,
        "height": 3.0,
        "velocity": 0.0
    })


# Belt-and-braces: even though the height cap already keeps
# the bars short, also push them behind the play button and
# every control drawn after it, so a bar can never visually
# paint over the buttons.

canvas.tag_lower(
    "eq_bar",
    play_outer
)


eq_phase = 0.0


def animate_equalizer():

    global eq_phase

    if not running:
        return


    eq_phase += 0.12


    playing = (
        not paused
        and pygame.mixer.music.get_busy()
    )


    for i, bar in enumerate(
        equalizer
    ):

        if playing:

            # Individual rectangular bar movement.
            # No curved/wavy visual shape.

            wave1 = (
                math.sin(
                    eq_phase
                    +
                    i * 0.52
                )
                + 1
            ) / 2


            wave2 = (
                math.sin(
                    eq_phase * 1.73
                    +
                    i * 0.91
                )
                + 1
            ) / 2


            target = (
                3
                +
                wave1 * 10
                +
                wave2 * 5
            )

        else:

            # Smooth decay when paused/stopped.

            target = 3


        # Spring-like smoothing

        difference = (
            target
            -
            bar["height"]
        )


        bar["velocity"] += (
            difference * 0.085
        )


        bar["velocity"] *= 0.78


        bar["height"] += (
            bar["velocity"]
        )


        if bar["height"] < 3:

            bar["height"] = 3

            bar["velocity"] = 0


        if bar["height"] > EQ_MAX_HEIGHT:

            bar["height"] = EQ_MAX_HEIGHT

            bar["velocity"] = 0


        x1, y1, x2, y2 = (
            canvas.coords(
                bar["id"]
            )
        )


        canvas.coords(
            bar["id"],
            x1,
            EQ_BOTTOM - bar["height"],
            x2,
            EQ_BOTTOM
        )


    window.after(
        25,
        animate_equalizer
    )


# ============================================================
# BOTTOM TAGLINE (LEFT)
# ============================================================
# Mirrors the "夢 / MUSIC HEALS WHAT WORDS CAN'T" caption in
# the bottom-left corner of the reference artwork.

canvas.create_line(
    30,
    655,
    30,
    678,
    fill=PINK,
    width=2
)

canvas.create_text(
    18,
    655,
    text="夢",
    anchor="nw",
    fill=PINK,
    font=("Arial", 14, "bold")
)

canvas.create_text(
    48,
    655,
    text="MUSIC HEALS",
    anchor="nw",
    fill=WHITE,
    font=("Arial", 8, "bold")
)

canvas.create_text(
    48,
    668,
    text="WHAT WORDS CAN'T",
    anchor="nw",
    fill="#8a747b",
    font=("Arial", 8)
)


# ============================================================
# BOTTOM TAGLINE (RIGHT)
# ============================================================
# Mirrors the "ECHO POD" wordmark + tiny bar icon in the
# bottom-right corner of the reference artwork.

canvas.create_text(
    495,
    655,
    text="ECHO POD",
    anchor="ne",
    fill=WHITE,
    font=("Arial", 8, "bold")
)

for i, bar_height in enumerate(
    [4, 7, 5, 9, 3]
):

    bx = 500 + i * 9

    canvas.create_rectangle(
        bx,
        676 - bar_height,
        bx + 4,
        676,
        fill=PINK,
        outline=""
    )


# ============================================================
# PLAYER UPDATE
# ============================================================

def update_player():

    if not running:
        return


    # --------------------------------------------------------
    # SONG FINISHED
    # --------------------------------------------------------

    for event in pygame.event.get():

        if event.type == SONG_FINISHED:

            if loop:

                pygame.mixer.music.play()

            else:

                next_song()

            return


    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    if not paused:

        position = (
            pygame.mixer.music.get_pos()
            /
            1000
        )


        if position < 0:

            position = 0


        if song_duration > 0:

            ratio = (
                position
                /
                song_duration
            )


            ratio = min(
                ratio,
                1
            )


            x = (
                PROGRESS_LEFT
                +
                (
                    PROGRESS_RIGHT
                    -
                    PROGRESS_LEFT
                )
                * ratio
            )


            canvas.coords(
                progress,
                PROGRESS_LEFT,
                PROGRESS_Y,
                x,
                PROGRESS_Y
            )


            canvas.coords(
                progress_dot,
                x - 6,
                PROGRESS_Y - 6,
                x + 6,
                PROGRESS_Y + 6
            )


        current_time.config(
            text=format_time(
                position
            )
        )


    window.after(
        80,
        update_player
    )


# ============================================================
# KEYBOARD
# ============================================================

def keyboard(event):

    key = event.keysym.lower()


    if key == "space":

        toggle_pause()


    elif key == "n":

        next_song()


    elif key == "p":

        previous_song()


    elif key == "s":

        toggle_shuffle()


    elif key == "l":

        toggle_loop()


    elif key == "escape":

        close_window()


window.bind_all(
    "<Key>",
    keyboard
)


# ============================================================
# CLOSE
# ============================================================

def close_window():

    global running

    running = False

    try:

        pygame.mixer.music.stop()

    except Exception:
        pass

    pygame.quit()

    window.destroy()


window.protocol(
    "WM_DELETE_WINDOW",
    close_window
)


# ============================================================
# START
# ============================================================

play_song()

update_shuffle()

update_loop()

animate_rain()

animate_equalizer()

update_player()

window.focus_force()

window.mainloop()
