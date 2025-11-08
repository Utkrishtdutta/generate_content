import argparse
import os
from instagrapi import Client
from app import create_post

# Instagram credentials
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")


# Initialize Instagram client
cl = Client()

def login_to_instagram():
    """Login to Instagram using the instagrapi client"""
    try:
        # Login to Instagram
        print(f"Logging in to Instagram as {INSTAGRAM_USERNAME}...")
        cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        print("Successfully logged in to Instagram")
        return True
    except Exception as e:
        print(f"Error logging in to Instagram: {e}")
        return False

def post_to_instagram(image_path, caption="Random Post"):
    """Post content to Instagram using instagrapi"""
    try:
        # Ensure we're logged in
        if not cl.user_id:
            logged_in = login_to_instagram()
            if not logged_in:
                return False
        
        # Upload the photo
        print(f"Uploading {image_path} to Instagram...")
        caption = caption + " #viral" + " #quoteofday"
        media = cl.photo_upload(
            path=image_path,
            caption=caption
        )
        
        print(f"Successfully posted to Instagram with caption: {caption}")
        print(f"Media ID: {media.id}")
        return True
            
    except Exception as e:
        print(f"Error posting to Instagram: {e}")
        
        # If posting failed due to login issues, try to login again
        if "login" in str(e).lower():
            print("Attempting to re-login...")
            login_success = login_to_instagram()
            if login_success:
                # Try posting again
                try:
                    media = cl.photo_upload(
                        path=image_path,
                        caption=caption
                    )
                    print(f"Successfully posted to Instagram after re-login")
                    return True
                except Exception as e2:
                    print(f"Error posting even after re-login: {e2}")
        
        return False
    

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
    
    image_path , caption= create_post(args.username)
    posted = post_to_instagram(image_path, caption)
    if posted:
        print(f"Image {image_path} has been posted on Insta")
    else:
        print(f"Image {image_path} has been not able to post on Insta")

if __name__ == "__main__":
    main()