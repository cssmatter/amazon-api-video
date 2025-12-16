# Video Configuration

# Video Settings
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
FPS = 30
SLIDE_DURATION = 4  # seconds per product

# Colors (RGB)
BACKGROUND_COLOR = (15, 23, 42)  # Dark blue-gray
GRADIENT_START = (15, 23, 42)  # Dark blue
GRADIENT_END = (30, 41, 59)  # Slightly lighter blue

# Text Colors
TITLE_COLOR = (255, 255, 255)  # White
CURRENT_PRICE_COLOR = (34, 197, 94)  # Green
ORIGINAL_PRICE_COLOR = (148, 163, 184)  # Gray
SAVINGS_COLOR = (251, 191, 36)  # Amber/Gold
BADGE_BG_COLOR = (220, 38, 38)  # Red
BADGE_TEXT_COLOR = (255, 255, 255)  # White

# Font Sizes
TITLE_FONT_SIZE = 45
CURRENT_PRICE_FONT_SIZE = 70
ORIGINAL_PRICE_FONT_SIZE = 40
SAVINGS_FONT_SIZE = 30
BADGE_FONT_SIZE = 60
LINK_TEXT_FONT_SIZE = 50

# Layout Positions (percentage of screen)
TITLE_Y_POS = 0.28  # Moved up slightly
CURRENT_PRICE_Y_POS = 0.52  # Moved down
ORIGINAL_PRICE_Y_POS = 0.64  # Moved down
SAVINGS_Y_POS = 0.77  # Moved down
BADGE_Y_POS = 0.08  # Moved up closer to top
LINK_TEXT_Y_POS = 0.92  # Bottom of screen

# Fonts
# MoviePy will use default fonts, but you can specify custom fonts here
FONT_FAMILY = "Arial-Bold"  # or path to .ttf file

# Output
OUTPUT_FILENAME = "amazon_deals_video.mp4"
CODEC = "libx264"
AUDIO = False  # No audio for now
BITRATE = "5000k"
