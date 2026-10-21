"""Tiny sound effects with no extra packages and no audio files.

Tones are generated as in-memory WAV data. On Windows they play through the standard
library's winsound (asynchronously); elsewhere the GUI falls back to the Tk bell.
Sounds are triggered only by confirmed server replies (see app.py), never by a click.
"""
import io
import math
import struct
import wave

try:
    import winsound
except ImportError:                      # not Windows
    winsound = None

RATE = 22050
NOTES = {          # name -> list of (frequency Hz, milliseconds)
    "x": [(660, 90)],
    "o": [(520, 90)],
    "new": [(392, 70), (523, 110)],
    "connect": [(440, 60), (660, 90)],
    "error": [(180, 160), (150, 160)],
    "win": [(523, 110), (659, 110), (784, 110), (1047, 260)],
    "draw": [(440, 140), (392, 140), (349, 220)],
    "resign": [(330, 140), (247, 260)],
}
_cache = {}


def make_wav(notes):
    """notes: [(hz, ms), ...] -> WAV bytes (16-bit mono, short fade to avoid clicks)."""
    frames = bytearray()
    for hz, ms in notes:
        n = int(RATE * ms / 1000)
        for i in range(n):
            fade = min(1.0, i / 120.0, (n - i) / 240.0)
            frames += struct.pack("<h", int(9000 * fade * math.sin(2 * math.pi * hz * i / RATE)))
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(bytes(frames))
    return buf.getvalue()


def play(kind, root=None):
    """Play a named effect. Never raises: sound must not break the game."""
    try:
        if winsound is not None:
            if kind not in _cache:
                _cache[kind] = make_wav(NOTES[kind])
            winsound.PlaySound(_cache[kind], winsound.SND_MEMORY | winsound.SND_ASYNC)
        elif root is not None:
            root.bell()
    except Exception:
        pass
