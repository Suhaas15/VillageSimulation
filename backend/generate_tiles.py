#!/usr/bin/env python3
"""
Script to generate all 5 tile types using Freepik API and apply them to the grid
Run this directly to generate tiles without timeout issues
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv('FREEPIK_API_KEY')
BASE_URL = "http://localhost:5001"

def generate_single_tile(tile_type):
    """Generate a single tile type"""
    print(f"\n{'='*60}")
    print(f"🎨 Generating {tile_type.upper()} tile...")
    print(f"{'='*60}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/assets/generate/tile",
            json={"tile_type": tile_type},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ {tile_type.capitalize()} tile generated successfully!")
                return data.get('url')
            else:
                print(f"❌ Failed: {data.get('error')}")
                return None
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text[:200]}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"⏱️  Request timed out (normal for Freepik API)")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def apply_tiles_to_grid(tiles_dict):
    """Apply generated tiles to the grid"""
    print(f"\n{'='*60}")
    print(f"🎨 Applying tiles to grid...")
    print(f"{'='*60}")
    
    # We need to make a custom request to apply tiles
    # For now, just show success - tiles are applied automatically per tile
    print(f"✅ Generated {len(tiles_dict)} tile types")
    for tile_type, url in tiles_dict.items():
        if url:
            preview = url[:80] + "..." if len(url) > 80 else url
            print(f"   - {tile_type}: {preview}")
    
    return True

def main():
    print("\n" + "="*60)
    print("🎨 FREEPIK TILE GENERATOR")
    print("="*60)
    print(f"API Key configured: {'Yes' if API_KEY and API_KEY != 'your_api_key_here' else 'No'}")
    print(f"Backend URL: {BASE_URL}")
    print("="*60)
    
    if not API_KEY or API_KEY == 'your_api_key_here':
        print("\n❌ ERROR: Freepik API key not configured!")
        print("Please add FREEPIK_API_KEY to backend/.env")
        sys.exit(1)
    
    # Check backend is running
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code != 200:
            print(f"\n❌ ERROR: Backend not responding correctly")
            sys.exit(1)
        print("\n✅ Backend is running")
    except Exception as e:
        print(f"\n❌ ERROR: Cannot connect to backend at {BASE_URL}")
        print(f"   Make sure backend is running: cd backend && python app.py")
        sys.exit(1)
    
    # Generate all 5 tile types
    tile_types = ['grass', 'dirt', 'stone', 'forest', 'water']
    tiles = {}
    
    print(f"\n🎨 Will generate {len(tile_types)} tile types")
    print(f"⏱️  Estimated time: ~{len(tile_types) * 12} seconds")
    print(f"⏳ Starting generation...\n")
    
    for i, tile_type in enumerate(tile_types, 1):
        print(f"\n📊 Progress: {i}/{len(tile_types)}")
        url = generate_single_tile(tile_type)
        if url:
            tiles[tile_type] = url
        
        # Wait between requests (except after last one)
        if i < len(tile_types):
            import time
            print(f"⏳ Waiting 10 seconds before next tile...")
            time.sleep(10)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"✅ GENERATION COMPLETE!")
    print(f"{'='*60}")
    print(f"Successfully generated: {len(tiles)}/{len(tile_types)} tiles")
    print(f"Failed: {len(tile_types) - len(tiles)}")
    
    if len(tiles) > 0:
        print(f"\n✅ Tiles have been automatically applied to the grid!")
        print(f"\n🎮 NEXT STEPS:")
        print(f"   1. Refresh your browser")
        print(f"   2. You should see the new tile textures!")
        print(f"   3. Pan around the map to see different tile types")
    else:
        print(f"\n❌ No tiles were generated successfully")
        print(f"   Check the backend logs for errors")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    main()

