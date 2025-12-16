
import moviepy
import inspect

print("MoviePy version:", moviepy.__version__)
try:
    from moviepy import afx
    print("afx imported from moviepy")
    print(dir(afx))
except ImportError:
    print("Could not import afx from moviepy")

try:
    import moviepy.audio.fx.all as afx_all
    print("Imported moviepy.audio.fx.all")
    print([x for x in dir(afx_all) if 'loop' in x.lower()])
except ImportError as e:
    print(f"Could not import moviepy.audio.fx.all: {e}")

try:
    from moviepy.audio.fx import AudioLoop
    print("Imported AudioLoop directly")
except ImportError as e:
    print(f"Could not import AudioLoop: {e}")
