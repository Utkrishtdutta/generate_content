import os
from PIL import Image, ImageDraw, ImageFont
import argparse
import json
from datetime import datetime
from groq import Groq

# Initialize the OpenAI client with the Groq base URL and your API key
def generate_text():
    client = Groq(
        api_key=os.getenv("GROQAPIKEY"),
    )

    # Make a chat completion request using a Groq-supported model
    prompt = f"""
You are an expert social media content creator. Your task is to generate a concise, thought-provoking quote for Instagram, targeting young adults (18+). The quote should be about life, relationships, career, growth, corporate Job and personal growth. Use a conversational, relatable, and authentic tone—like candid advice from a trusted friend. Limit the quote to 20 words or fewer. If relevant, include 1-2 emojis that genuinely enhance the message.

Requirements:
- Choose different colors for background_color and text_color to make the post more engaging.
- Maximize engagement and shareability.
- Do not use explicit or offensive language.

Context:
- Today’s date: {datetime.now().date().strftime("%d-%m-%y")}
- Day of the week: {datetime.now().strftime("%A")}

Example quotes:
- "Maybe your future husband is in your pending friend request."
- "Love your partner like they feels heaven."
- "Nobody gets angrier than a woman being accused of something she actually did."
- "Women reject 50 men, avoid 20 walking red flags, and still choose the deluxe red flag package."

Output format (JSON):
{{
  "quote": "<Your quote here>",
  "hashtag": "<Relevant hashtags, e.g. #viral #quote>",
  "background_color": "<Suggested background color> eg. black, white",
  "text_color": "<Suggested text color> eg. red, blue"
}}
"""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt,
            }
        ],
        model="openai/gpt-oss-20b",  # Use a Groq-supported model
    )
    return chat_completion.choices[0].message.content


def create_post(username="random_tweet"):
    """
    Create a social media style post image with custom text
    
    Args:
        text: The text to display on the image
        output_path: Path to save the output image
        username: Username to display at the bottom
    """
    text = json.loads(generate_text())
    # Image dimensions
    print("Text: ", text)
    # print(json.loads(text))
    width, height = 1080, 1080
    
    # Create image with dark background
    img = Image.new('RGB', (width, height), color=text['background_color'])
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fallback to default if not available
    try:
        # Try different font paths for different systems
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
            "/System/Library/Fonts/Helvetica.ttc",  # macOS
            "C:\\Windows\\Fonts\\arial.ttf",  # Windows
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"  # Linux alternative
        ]
        
        font = None
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, 56)
                break
            except:
                continue
        
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Wrap text to fit width
    margin = 100
    max_width = width - (2 * margin)
    
    # Split text into lines that fit
    words = text['quote'].split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        text_width = bbox[2] - bbox[0]
        
        if text_width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Calculate total height of text block
    line_height = 80
    total_text_height = len(lines) * line_height
    
    # Start position (centered vertically)
    y = (height - total_text_height) // 2
    
    # Draw each line centered
    for line in lines:
        print("line: ", line)
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        # Draw text in black
        draw.text((x, y), line, fill=text['text_color'], font=font, embedded_color=True)
        y += line_height
    
    # Add watermark at bottom right
    try:
        watermark_font = ImageFont.truetype(font_paths[0], 96)
    except:
        watermark_font = ImageFont.load_default()

    
    watermark_text = f"@{username}"
    bbox = draw.textbbox((0, 0), watermark_text, font=watermark_font)
    watermark_width = bbox[2] - bbox[0]
    
    draw.text(
        (width - watermark_width - 40, height - 60),
        watermark_text,
        fill=(200, 200, 200),
        font=watermark_font,
        embedded_color=True
    )
    
    # Save the image
    output_path = f'post/{datetime.now().date()}.png'
    img.save(output_path, quality=200)
    print(f"Image saved to: {output_path}")
    return output_path, text['quote'] + " " + text['hashtag']

def main():
    parser = argparse.ArgumentParser(
        description='Generate a social media post image with custom text'
    )
    parser.add_argument(
        '-u', '--username',
        type=str,
        default='mayank_tweet',
        help='Username for watermark (default: mayank_tweet)'
    )
    
    args = parser.parse_args()
    
    create_post(args.username)

if __name__ == "__main__":
    main()