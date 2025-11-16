import requests
import time
import os
import json
from typing import List, Optional, Dict

class FreepikAPI:
    """Wrapper for Freepik API to generate images and remove backgrounds"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.freepik.com/v1"
        self.headers = {
            "X-Freepik-API-Key": api_key,
            "Content-Type": "application/json"
        }
        
        # Optimized prompts for sprite generation - ONLY ONE TREE PER IMAGE
        # Pure white background (#FFFFFF) for CSS-based transparency
        self.tree_prompts = [
            "A single tree, only one tree, pixel art sprite in 16-bit retro game style, ONE deciduous tree perfectly centered on PURE SOLID WHITE BACKGROUND #FFFFFF, vibrant lime green leafy canopy with darker green shadows, brown trunk with light bark texture, rounded bushy crown, clean symmetrical shape, isolated single object, no forest, no multiple trees, no ground, no grass, sharp pixel edges, game asset, flat studio lighting, completely white background, NOT multiple trees, just ONE tree sprite, white background only, 512x512",
            "ONE oak tree sprite only, not multiple trees, pixel art in classic RPG game style, single wide oak tree with spreading canopy, rich forest green leaves with yellow-green highlights, thick brown trunk with bark details, rounded bushy silhouette, centered composition on PURE WHITE #FFFFFF SOLID BACKGROUND, no shadows on ground, no grass, only one tree visible, not a forest, game sprite asset, detailed pixel shading, clean edges, retro 16-bit aesthetic, completely white background, 512x512",
            "ONE pine tree only, single coniferous evergreen sprite, pixel art with distinct triangular Christmas tree shape, tiered horizontal branch layers, deep forest green needles, thin brown trunk, pointed top, centered on SOLID WHITE #FFFFFF BACKGROUND, simple flat lighting, no other trees, not multiple trees, isolated single pine tree sprite, game asset, crisp pixel definition, 90s JRPG visual style, just one tree, pure white background, no grass, 512x512"
        ]
        
        self.tile_prompts = {
            'grass': "Seamless tileable pixel art grass texture for game terrain, top-down aerial view, lush vibrant green lawn with varied blade directions creating natural organic pattern, subtle color variation using light lime green and darker forest green pixels, soft dithered shading suggesting gentle undulation, small random darker spots for depth, perfectly repeating edges that tile infinitely without visible seams, no flowers or objects, flat even lighting, 16-bit retro game aesthetic, 256x256 seamless pattern, uniform grass coverage",
            'dirt': "Seamless tileable pixel art dirt ground texture for game terrain, top-down aerial view, rich brown earth surface with natural variation, warm brown and tan color palette with darker shadows, small pebbles and tiny rocks scattered randomly, rough earthy texture with subtle grain, perfectly repeating edges that tile infinitely without visible seams, no plants or grass or objects, flat even lighting, 16-bit retro game aesthetic, 256x256 seamless pattern, uniform dirt coverage, natural soil appearance",
            'stone': "Seamless tileable pixel art stone pavement texture for game terrain, top-down aerial view, gray cobblestone or flagstone surface, varied stone sizes creating natural pattern, light gray to dark gray color palette with subtle highlights, cracks and weathering between stones, rough rocky texture with depth, perfectly repeating edges that tile infinitely without visible seams, no objects or plants, flat even lighting, 16-bit retro game aesthetic, 256x256 seamless pattern, medieval stone path style",
            'forest': "Seamless tileable pixel art forest floor texture for game terrain, top-down aerial view, dark mossy ground with scattered leaf litter, deep forest green and brown color palette, patches of moss mixed with dark soil, small fallen leaves and organic debris, natural woodland texture with depth, perfectly repeating edges that tile infinitely without visible seams, no trees or large objects, flat even lighting, 16-bit retro game aesthetic, 256x256 seamless pattern, dense forest ground appearance",
            'water': "Seamless tileable pixel art water surface texture for game terrain, top-down aerial view, calm blue water with gentle ripple patterns, bright cyan and deep blue color palette with subtle highlights, animated-style wave texture suggesting gentle movement, reflective surface with light sparkles, perfectly repeating edges that tile infinitely without visible seams, no objects or land, flat even lighting, 16-bit retro game aesthetic, 256x256 seamless pattern, peaceful water appearance"
        }
    
    def generate_image(self, prompt: str) -> Optional[str]:
        """
        Generate an image using Freepik AI Image Generation API
        
        Args:
            prompt: Text prompt for image generation
            
        Returns:
            URL of generated image or None if failed
        """
        if not self.api_key or self.api_key == 'your_api_key_here':
            print("⚠️  No Freepik API key configured")
            return None
        
        try:
            # Freepik AI Image Generation endpoint
            url = f"{self.base_url}/ai/text-to-image"
            
            payload = {
                "prompt": prompt,
                "num_images": 1,
                "image": {
                    "size": "square"
                }
            }
            
            print(f"🎨 Generating image: {prompt[:60]}...")
            response = requests.post(url, json=payload, headers=self.headers, timeout=60)
            
            print(f"📥 Image generation response status: {response.status_code}")
            
            if response.status_code == 200 or response.status_code == 201:
                result = response.json()
                print(f"📥 Response keys: {list(result.keys())}")
                
                # Handle different response formats
                if "data" in result and isinstance(result["data"], list) and len(result["data"]) > 0:
                    image_url = result["data"][0].get("url") or result["data"][0].get("base64")
                    print(f"📥 Image format: {'URL' if 'url' in result['data'][0] else 'base64'}")
                elif "data" in result and "url" in result["data"]:
                    image_url = result["data"]["url"]
                    print(f"📥 Image format: URL")
                elif "data" in result and "base64" in result["data"]:
                    image_url = result["data"]["base64"]
                    print(f"📥 Image format: base64")
                else:
                    print(f"⚠️  Unexpected response format. Keys: {result.keys()}")
                    print(f"⚠️  Response sample: {str(result)[:300]}")
                    return None
                
                # Fix base64 data - ensure it has proper data URI prefix
                if image_url and not image_url.startswith(('http://', 'https://', 'data:')):
                    image_url = f"data:image/png;base64,{image_url}"
                    print(f"✅ Added data URI prefix to base64 image")
                
                print(f"✅ Image generated successfully!")
                print(f"✅ Image type: {'base64' if image_url.startswith('data:') else 'URL'}")
                print(f"✅ Preview: {image_url[:80]}...")
                return image_url
            else:
                print(f"❌ Freepik API error:")
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text[:500]}")
                return None
                
        except Exception as e:
            print(f"❌ Exception generating image: {e}")
            return None
    
    def remove_background(self, image_url: str) -> Optional[str]:
        """
        Remove background from image using Freepik Background Removal API
        
        API Documentation: https://docs.freepik.com/api-reference/ai-beta-remove-background
        - Endpoint: /v1/ai/beta/remove-background
        - Content-Type: application/x-www-form-urlencoded
        - Requires: image_url (must be a public URL, NOT base64)
        
        Args:
            image_url: URL of image to process (must be hosted URL, not base64)
            
        Returns:
            URL of transparent PNG or original if failed
        """
        if not self.api_key or self.api_key == 'your_api_key_here':
            print("⚠️  No Freepik API key configured")
            return image_url
        
        # Freepik API ONLY accepts hosted URLs, not base64
        if image_url and image_url.startswith('data:'):
            print("ℹ️  Skipping background removal - Freepik API requires hosted URL (not base64)")
            print("💡 The image has pure white background - will use CSS blend mode in frontend")
            return image_url
        
        # If it's a hosted URL, try background removal
        try:
            # Use the correct beta endpoint with form-urlencoded content type
            url = f"{self.base_url}/ai/beta/remove-background"
            
            # Use form-urlencoded format (not JSON)
            headers = {
                "X-Freepik-API-Key": self.api_key,
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            # Send as form data
            data = {
                "image_url": image_url
            }
            
            print(f"🔄 Removing background from image...")
            print(f"📤 Using endpoint: {url}")
            print(f"📤 Image URL: {image_url[:80]}...")
            
            response = requests.post(url, data=data, headers=headers, timeout=60)
            
            print(f"📥 Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"📥 Response keys: {list(result.keys())}")
                
                # Get the high-resolution URL (or url field as fallback)
                clean_url = result.get("high_resolution") or result.get("url")
                
                if clean_url:
                    print(f"✅ Background removed successfully!")
                    print(f"✅ Transparent image URL: {clean_url[:80]}...")
                    return clean_url
                else:
                    print(f"⚠️  No image URL in response: {result}")
                    return image_url
            else:
                print(f"❌ Background removal API error:")
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text[:500]}")
                return image_url
                
        except Exception as e:
            print(f"❌ Exception removing background: {str(e)}")
            import traceback
            print(f"   Traceback: {traceback.format_exc()[:300]}")
            return image_url
    
    def generate_tiles(self, tile_type: str, count: int = 1) -> List[str]:
        """
        Generate tile images (no background removal needed - tiles should have full backgrounds)
        
        Args:
            tile_type: Type of tile (grass, dirt, stone, forest, water)
            count: Number of variations to generate (default 1)
            
        Returns:
            List of image URLs
        """
        prompt = self.tile_prompts.get(tile_type, self.tile_prompts['grass'])
        
        tile_urls = []
        
        for i in range(count):
            try:
                tile_url = self.generate_image(prompt)
                if tile_url:
                    tile_urls.append(tile_url)
                else:
                    # Fallback to placeholder
                    tile_urls.append(self._get_placeholder(tile_type))
            except Exception as e:
                print(f"⚠️  Error generating {tile_type} tile {i}: {e}")
                tile_urls.append(self._get_placeholder(tile_type))
        
        return tile_urls
    
    def generate_tree_sprites(self) -> List[str]:
        """
        Generate 3 tree sprites with background removal
        
        Returns:
            List of 3 transparent tree sprite URLs
        """
        trees = []
        
        for i, prompt in enumerate(self.tree_prompts, 1):
            try:
                print(f"🌳 Generating tree sprite {i}/3...")
                
                # Step 1: Generate image
                img_url = self.generate_image(prompt)
                
                # Wait 10 seconds after image generation
                if img_url:
                    print(f"⏳ Waiting 10 seconds before background removal...")
                    time.sleep(10)
                
                if img_url:
                    # Step 2: Remove background
                    clean_url = self.remove_background(img_url)
                    trees.append(clean_url)
                    print(f"✅ Tree sprite {i} complete")
                else:
                    print(f"⚠️  Tree sprite {i} generation failed, using placeholder")
                    trees.append("/tree.png")  # Fallback to user's tree
                
                # Wait 10 seconds before next tree
                if i < len(self.tree_prompts):
                    print(f"⏳ Waiting 10 seconds before next tree...")
                    time.sleep(10)
                    
            except Exception as e:
                print(f"❌ Error generating tree sprite {i}: {e}")
                trees.append("/tree.png")  # Fallback
        
        return trees
    
    def generate_environment_assets(self) -> Dict[str, List[str]]:
        """
        Generate all environment assets: 3 tile types (no trees for now)
        
        Total API calls: 3 (one for each tile type)
        - Grass, Dirt, Water
        
        Returns:
            Dictionary with 'trees' and 'tiles' keys containing URLs
        """
        print("🎨 Starting environment asset generation...")
        print("📊 Total API calls to be made: 3")
        print("   🟩 Grass tile")
        print("   🟫 Dirt tile")
        print("   💧 Water tile")
        
        tiles = {}
        tile_types = ['grass', 'dirt', 'water']
        
        for i, tile_type in enumerate(tile_types, 1):
            try:
                print(f"\n=== GENERATING {tile_type.upper()} TILE ({i}/3) ===")
                print(f"🎨 API Call {i}/3: Generating {tile_type} tile...")
                
                tile_url = self.generate_image(self.tile_prompts[tile_type])
            
                if tile_url:
                    tiles[tile_type] = tile_url
                    print(f"✅ {tile_type.capitalize()} tile generated successfully!")
                else:
                    print(f"⚠️ {tile_type.capitalize()} tile generation failed, using placeholder")
                    tiles[tile_type] = self._get_placeholder(tile_type)
                
                # Wait 10 seconds between tiles (except after last one)
                if i < len(tile_types):
                    print(f"⏳ Waiting 10 seconds before next tile...")
                    time.sleep(10)
                
            except Exception as e:
                print(f"❌ Error generating {tile_type} tile: {e}")
                tiles[tile_type] = self._get_placeholder(tile_type)
        
        print("\n✅ Asset generation complete!")
        print(f"   - Trees: 0 (using default tree.png)")
        print(f"   - Tiles: {len(tiles)}")
        
        return {
            "trees": [],
            "tiles": tiles
        }
    
    def generate_all_tiles(self) -> Dict[str, str]:
        """
        Generate all 5 tile types (grass, dirt, stone, forest, water)
        
        Returns:
            Dictionary with tile_type as key and image URL as value
        """
        print("🎨 Starting tile generation for all types...")
        print(f"📊 Total API calls to be made: {len(self.tile_prompts)}")
        
        tiles = {}
        tile_types = ['grass', 'dirt', 'stone', 'forest', 'water']
        
        for i, tile_type in enumerate(tile_types, 1):
            try:
                print(f"\n=== GENERATING {tile_type.upper()} TILE ({i}/{len(tile_types)}) ===")
                print(f"🎨 API Call {i}/{len(tile_types)}: Generating {tile_type} tile...")
                
                tile_url = self.generate_image(self.tile_prompts[tile_type])
                
                if tile_url:
                    tiles[tile_type] = tile_url
                    print(f"✅ {tile_type.capitalize()} tile generated successfully!")
                else:
                    print(f"⚠️ {tile_type.capitalize()} tile generation failed, using placeholder")
                    tiles[tile_type] = self._get_placeholder(tile_type)
                
                # Wait 10 seconds between API calls to avoid rate limiting
                if i < len(tile_types):
                    print(f"⏳ Waiting 10 seconds before next tile...")
                    time.sleep(10)
                    
            except Exception as e:
                print(f"❌ Error generating {tile_type} tile: {e}")
                tiles[tile_type] = self._get_placeholder(tile_type)
        
        print("\n✅ All tile generation complete!")
        print(f"   - Tiles generated: {len(tiles)}")
        
        return tiles
    
    def _get_placeholder(self, tile_type: str) -> str:
        """Return placeholder URL for tile type"""
        placeholders = {
            'grass': "https://via.placeholder.com/192x192/7cb342/FFFFFF?text=Grass",
            'dirt': "https://via.placeholder.com/192x192/8d6e63/FFFFFF?text=Dirt",
            'stone': "https://via.placeholder.com/192x192/795548/FFFFFF?text=Stone",
            'forest': "https://via.placeholder.com/192x192/558b2f/FFFFFF?text=Forest",
            'water': "https://via.placeholder.com/192x192/42a5f5/FFFFFF?text=Water"
        }
        return placeholders.get(tile_type, "https://via.placeholder.com/192x192/CCCCCC/000000?text=Tile")
