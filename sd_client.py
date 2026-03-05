import os
import sys
import json
import argparse
import requests
from pathlib import Path
from PIL import Image
import base64
from io import BytesIO

# Configuration
SD_API_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"
DEFAULT_OUTPUT_DIR = "output"
DEFAULT_FILENAME = "generated_image.png"

def generate_image(prompt, negative_prompt="", steps=20, cfg_scale=7, width=512, height=512):
    """
    Generate an image using the local Stable Diffusion API
    
    Args:
        prompt (str): The text prompt for image generation
        negative_prompt (str): Things to avoid in the image
        steps (int): Number of diffusion steps (20-30 is good)
        cfg_scale (int): How closely to follow the prompt (7 is a good balance)
        width (int): Width of the generated image
        height (int): Height of the generated image
        
    Returns:
        dict: Contains 'image' (PIL Image) and 'info' (generation parameters)
    """
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "width": width,
        "height": height,
        "sampler_name": "Euler a",
        "enable_hr": False,
        "denoising_strength": 0.7,
        "seed": -1,
    }
    
    try:
        print(f"Sending request to Stable Diffusion API...")
        response = requests.post(SD_API_URL, json=payload)
        response.raise_for_status()
        r = response.json()
        
        if 'images' not in r or not r['images']:
            print("Error: No images in response")
            print(f"Response: {r}")
            return None
            
        # Convert base64 to PIL Image
        image_data = r['images'][0].split(",", 1)[1] if "," in r['images'][0] else r['images'][0]
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        
        return {
            'image': image,
            'info': r.get('info', {})
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Stable Diffusion API: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        import traceback
        traceback.print_exc()
        
    return None

def save_image(image, filepath):
    """Save PIL image to file"""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save the image
        image.save(filepath)
        print(f"Image saved to: {filepath}")
        return filepath
    except Exception as e:
        print(f"Error saving image: {str(e)}")
        return None

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate images using Stable Diffusion')
    parser.add_argument('--prompt', type=str, required=True, help='Text prompt for image generation')
    parser.add_argument('--negative_prompt', type=str, default="", help='Negative prompt')
    parser.add_argument('--steps', type=int, default=20, help='Number of diffusion steps')
    parser.add_argument('--cfg_scale', type=float, default=7.0, help='CFG scale')
    parser.add_argument('--width', type=int, default=512, help='Image width')
    parser.add_argument('--height', type=int, default=512, help='Image height')
    parser.add_argument('--output_dir', type=str, default=DEFAULT_OUTPUT_DIR, help='Output directory')
    parser.add_argument('--filename', type=str, default=DEFAULT_FILENAME, help='Output filename')
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Generate the image
    result = generate_image(
        prompt=args.prompt,
        negative_prompt=args.negative_prompt,
        steps=args.steps,
        cfg_scale=args.cfg_scale,
        width=args.width,
        height=args.height
    )
    
    if result and result['image']:
        # Save the image
        output_path = os.path.join(args.output_dir, args.filename)
        saved_path = save_image(result['image'], output_path)
        
        if saved_path:
            # Print the path so Node.js can capture it
            print(f"Generated image: {saved_path}")
            sys.exit(0)
        else:
            print("Failed to save image")
            sys.exit(1)
    else:
        print("Failed to generate image")
        sys.exit(1)

if __name__ == "__main__":
    main()
