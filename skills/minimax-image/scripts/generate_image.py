#!/usr/bin/env python3
"""
MiniMax Image Generation Script
Generates images using MiniMax Image-01 API
"""

import os
import sys
import json
import argparse
import base64
import re
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Configuration
API_KEY = os.environ.get("MINIMAX_API_KEY")
if not API_KEY:
    print("Error: MINIMAX_API_KEY environment variable not set", file=sys.stderr)
    sys.exit(1)

BASE_URL = "https://api.minimax.io/v1/image_generation"

def generate_image(
    prompt: str,
    aspect_ratio: str = "1:1",
    n_images: int = 1,
    response_format: str = "url",
    output_dir: str = None
) -> dict:
    """
    Generate image(s) using MiniMax Image-01 API.
    
    Args:
        prompt: Text description of the desired image
        aspect_ratio: Image aspect ratio (1:1, 16:9, 4:3, 3:2, 2:3)
        n_images: Number of images to generate (1-9)
        response_format: "url" or "base64"
        output_dir: Directory to save images (defaults to current directory)
    
    Returns:
        Dictionary with results and file paths
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "image-01",
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "n_images": n_images,
        "response_format": response_format
    }
    
    try:
        req = Request(
            BASE_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        with urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
            
    except HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else "Unknown error"
        print(f"API Error ({e.code}): {error_body}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Network Error: {e.reason}", file=sys.stderr)
        sys.exit(1)
    
    # Process results
    if response_format == "url":
        image_urls = (result.get("data") or {}).get("image_urls") or []
        files_saved = []
        
        for i, img_url in enumerate(image_urls):
            if img_url:
                print(f"  Image {i+1}: {img_url}")
                files_saved.append({"index": i+1, "url": img_url, "type": "url"})
        
        return {
            "success": True,
            "count": len(files_saved),
            "images": files_saved,
            "prompt": prompt
        }
    
    elif response_format == "base64":
        images_b64 = result.get("data", [])
        files_saved = []
        
        if output_dir is None:
            output_dir = os.getcwd()
        
        os.makedirs(output_dir, exist_ok=True)
        
        for i, item in enumerate(images_b64):
            b64_data = item.get("b64_image", "")
            if b64_data:
                filename = f"minimax_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i+1}.png"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, "wb") as f:
                    f.write(base64.b64decode(b64_data))
                
                print(f"  Image {i+1}: {filepath}")
                files_saved.append({"index": i+1, "path": filepath, "type": "file"})
        
        return {
            "success": True,
            "count": len(files_saved),
            "images": files_saved,
            "prompt": prompt
        }
    
    return {"success": False, "error": "Unknown response format"}


def main():
    parser = argparse.ArgumentParser(description="Generate images using MiniMax Image-01 API")
    parser.add_argument("--prompt", "-p", required=True, help="Image description text")
    parser.add_argument("--aspect-ratio", "-a", default="1:1", 
                        choices=["1:1", "16:9", "4:3", "3:2", "2:3"],
                        help="Image aspect ratio (default: 1:1)")
    parser.add_argument("--count", "-c", type=int, default=1, choices=range(1, 10),
                        help="Number of images to generate (1-9, default: 1)")
    parser.add_argument("--format", "-f", default="url", choices=["url", "base64"],
                        help="Response format: url or base64 (default: url)")
    parser.add_argument("--output-dir", "-o", default=None,
                        help="Directory to save base64 images")
    
    args = parser.parse_args()
    
    # Remove leading/trailing quotes if present (common when passing multi-word prompts)
    prompt = args.prompt.strip('"\'')
    
    print(f"Generating {args.count} image(s) with aspect ratio {args.aspect_ratio}...")
    print(f"Prompt: {prompt}")
    print()
    
    result = generate_image(
        prompt=prompt,
        aspect_ratio=args.aspect_ratio,
        n_images=args.count,
        response_format=args.format,
        output_dir=args.output_dir
    )
    
    print()
    if result["success"]:
        print(f"✅ Successfully generated {result['count']} image(s)")
    else:
        print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
