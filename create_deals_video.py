"""
Amazon Deals Video Generator
Creates a YouTube-ready slider video showing product deals
Each product is displayed for 4 seconds with pricing information
"""

import json
import moviepy
from moviepy import ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips
import numpy as np
import video_config


def load_deals(filename="products.json"):
    """Load deals from JSON file."""
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['products']


def create_gradient_background(width, height):
    """Create a gradient background image."""
    # Create gradient from top to bottom
    gradient = np.zeros((height, width, 3), dtype=np.uint8)
    
    start_color = np.array(video_config.GRADIENT_START)
    end_color = np.array(video_config.GRADIENT_END)
    
    for y in range(height):
        # Linear interpolation between start and end colors
        ratio = y / height
        color = start_color * (1 - ratio) + end_color * ratio
        gradient[y, :] = color.astype(np.uint8)
    
    return gradient


def create_product_slide(product, width, height, duration):
    """
    Create a video clip for a single product.
    
    Args:
        product: Product dictionary with deal information
        width: Video width
        height: Video height
        duration: Slide duration in seconds
        
    Returns:
        VideoClip: Video clip for this product
    """
    # Create background
    background = create_gradient_background(width, height)
    bg_clip = ImageClip(background, duration=duration)
    
    # Create text clips
    clips = [bg_clip]
    
    # Title
    title_text = product['title']
    # Truncate if too long
    if len(title_text) > 60:
        title_text = title_text[:57] + "..."
    # Add spaces to help with bounding box
    title_text = title_text + "   "
    
    try:
        title_clip = TextClip(
            text=title_text,
            font_size=video_config.TITLE_FONT_SIZE,
            color='white',
            size=(width - 200, None),
            method='caption',
            text_align='center'
        ).with_position(('center', int(height * video_config.TITLE_Y_POS))).with_duration(duration)
        clips.append(title_clip)
    except Exception as e:
        print(f"    Warning: Could not create title clip: {e}")
    
    # Current Price (Large and Green)
    try:
        current_price_clip = TextClip(
            text=product['current_price'] + " ",  # Add space to prevent clipping
            font_size=video_config.CURRENT_PRICE_FONT_SIZE,
            color='#22C55E',  # Green
            text_align='center'
        ).with_position(('center', int(height * video_config.CURRENT_PRICE_Y_POS))).with_duration(duration)
        clips.append(current_price_clip)
    except Exception as e:
        print(f"    Warning: Could not create price clip: {e}")
    
    # Original Price (Strikethrough effect with smaller text)
    if product.get('original_price'):
        try:
            original_text = f"Was: {product['original_price']}"
            original_price_clip = TextClip(
                text=original_text,
                font_size=video_config.ORIGINAL_PRICE_FONT_SIZE,
                color='#94A3B8',  # Gray
                text_align='center'
            ).with_position(('center', int(height * video_config.ORIGINAL_PRICE_Y_POS))).with_duration(duration)
            clips.append(original_price_clip)
        except Exception as e:
            print(f"    Warning: Could not create original price clip: {e}")
    
    # Savings Information
    if product.get('savings') and product.get('savings_percentage'):
        try:
            savings_text = f"Save {product['savings']} ({product['savings_percentage']})"
            savings_clip = TextClip(
                text=savings_text,
                font_size=video_config.SAVINGS_FONT_SIZE,
                color='#FBBF24',  # Amber/Gold
                text_align='center'
            ).with_position(('center', int(height * video_config.SAVINGS_Y_POS))).with_duration(duration)
            clips.append(savings_clip)
        except Exception as e:
            print(f"    Warning: Could not create savings clip: {e}")
    
    # Savings Percentage Badge (Top)
    if product.get('savings_percentage'):
        try:
            badge_text = f"{product['savings_percentage']} OFF"
            badge_clip = TextClip(
                text=badge_text,
                font_size=video_config.BADGE_FONT_SIZE,
                color='white',
                bg_color='#DC2626',  # Red background
                size=(400, 120),
                method='caption',
                text_align='center'
            ).with_position(('center', int(height * video_config.BADGE_Y_POS))).with_duration(duration)
            clips.append(badge_clip)
        except Exception as e:
            print(f"    Warning: Could not create badge clip: {e}")
    
    # Prime Badge if eligible
    try:
        if product.get('is_prime_eligible'):
            prime_clip = TextClip(
                text="Prime Eligible",
                font_size=35,
                color='white',
                bg_color='#0F9D58',  # Green
                size=(250, 60),
                method='caption'
            ).with_position((width - 300, height - 100)).with_duration(duration)
            clips.append(prime_clip)
    except Exception as e:
        print(f"    Warning: Could not create prime clip: {e}")

    # Link in Description Text
    try:
        link_text_clip = TextClip(
            text="Product Link in Description",
            font_size=video_config.LINK_TEXT_FONT_SIZE,
            color='white',
            text_align='center'
        ).with_position(('center', int(height * video_config.LINK_TEXT_Y_POS))).with_duration(duration)
        clips.append(link_text_clip)
    except Exception as e:
        print(f"    Warning: Could not create link text clip: {e}")
    
    # Composite all clips - only use background if no text clips were created
    if len(clips) == 1:
        final_clip = bg_clip
    else:
        final_clip = CompositeVideoClip(clips)
    
    # Add fade in/out
    # try:
    #     final_clip = final_clip.fadein(0.3).fadeout(0.3)
    # except:
    #     pass  # Fade effects are optional
    
    return final_clip


def create_intro_slide(width, height, duration=3):
    """Create an intro slide."""
    background = create_gradient_background(width, height)
    bg_clip = ImageClip(background, duration=duration)
    
    try:
        title_clip = TextClip(
            text="Amazon Deals",
            font_size=120,
            color='white'
        ).with_position(('center', int(height * 0.35))).with_duration(duration)
        
        subtitle_clip = TextClip(
            text="Today's Best Offers",
            font_size=60,
            color='#FBBF24'
        ).with_position(('center', int(height * 0.55))).with_duration(duration)
        
        final_clip = CompositeVideoClip([bg_clip, title_clip, subtitle_clip])
        # final_clip = final_clip.fadein(0.5).fadeout(0.5)
    except Exception as e:
        print(f"Warning: Could not create intro with text: {e}")
        final_clip = bg_clip
    
    return final_clip


def create_outro_slide(width, height, duration=3):
    """Create an outro slide."""
    background = create_gradient_background(width, height)
    bg_clip = ImageClip(background, duration=duration)
    
    try:
        title_clip = TextClip(
            text="Thanks for Watching!",
            font_size=100,
            color='white'
        ).with_position(('center', int(height * 0.35))).with_duration(duration)
        
        subtitle_clip = TextClip(
            text="Check description for links",
            font_size=50,
            color='#FBBF24'
        ).with_position(('center', int(height * 0.55))).with_duration(duration)
        
        final_clip = CompositeVideoClip([bg_clip, title_clip, subtitle_clip])
        # final_clip = final_clip.fadein(0.5).fadeout(0.5)
    except Exception as e:
        print(f"Warning: Could not create outro with text: {e}")
        final_clip = bg_clip
    
    return final_clip


def create_deals_video(input_file="products.json", output_file=None):
    """
    Create a video from deals data.
    
    Args:
        input_file: Path to products.json
        output_file: Output video filename
    """
    if output_file is None:
        output_file = video_config.OUTPUT_FILENAME
    
    print("=" * 60)
    print("Amazon Deals Video Generator")
    print("=" * 60)
    
    # Load deals
    print(f"\nLoading deals from {input_file}...")
    deals = load_deals(input_file)
    print(f"Found {len(deals)} deals")
    
    # Create video clips
    print("\nCreating video slides...")
    clips = []
    
    # Intro
    print("  Creating intro slide...")
    intro = create_intro_slide(video_config.VIDEO_WIDTH, video_config.VIDEO_HEIGHT)
    clips.append(intro)
    
    # Product slides
    for i, product in enumerate(deals, 1):
        print(f"  [{i}/{len(deals)}] Creating slide for: {product['title'][:40]}...")
        slide = create_product_slide(
            product,
            video_config.VIDEO_WIDTH,
            video_config.VIDEO_HEIGHT,
            video_config.SLIDE_DURATION
        )
        clips.append(slide)
    
    # Outro
    print("  Creating outro slide...")
    outro = create_outro_slide(video_config.VIDEO_WIDTH, video_config.VIDEO_HEIGHT)
    clips.append(outro)
    
    # Concatenate all clips
    print("\nCombining all slides...")
    # Use method="chain" which is more memory efficient than "compose"
    final_video = concatenate_videoclips(clips, method="chain")
    
    # Calculate total duration
    total_duration = len(deals) * video_config.SLIDE_DURATION + 6  # +6 for intro/outro
    print(f"Total video duration: {total_duration} seconds ({total_duration/60:.1f} minutes)")
    
    # Write video file
    print(f"\nRendering video to {output_file}...")
    print("This may take a few minutes...")
    
    final_video.write_videofile(
        output_file,
        fps=video_config.FPS,
        codec=video_config.CODEC,
        bitrate=video_config.BITRATE,
        audio=video_config.AUDIO,
        threads=1,
        preset='medium',
        logger='bar'
    )
    
    print("\n" + "=" * 60)
    print(f"Video created successfully: {output_file}")
    print("=" * 60)
    print(f"\nVideo specs:")
    print(f"  Resolution: {video_config.VIDEO_WIDTH}x{video_config.VIDEO_HEIGHT}")
    print(f"  Duration: {total_duration} seconds")
    print(f"  Products: {len(deals)}")
    print(f"  Slide duration: {video_config.SLIDE_DURATION} seconds each")
    print("\nReady to upload to YouTube!")


def main():
    """Main function."""
    create_deals_video()


if __name__ == "__main__":
    main()
