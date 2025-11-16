"""
Oracle Environment Analyzer
Calls Airia AI API to analyze the game world and determine optimal oracle placement
"""

import os
import requests
import json
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

ORACLE_SYSTEM_PROMPT = """You are The Oracle, the central intelligence of the autonomous AI Village simulation.

Your first responsibility is to understand the environment by analyzing the initial world layout.

You receive the following input:

{
"tree_locations": [ { "x": int, "y": int }, ... ],
"terrain_tiles": [ ... ],
"map_width": int,
"map_height": int
}

Your goals:

1. Analyze the spatial layout.

2. Identify possible safe spawn positions for yourself (avoid trees).

3. Select the best Oracle spawn location using these rules:

- Must not collide with a tree.
- Prefer central coordinates on the map.
- Prefer an open tile with maximum walking accessibility.
- If multiple candidates exist, choose the closest to exact center.

4. Create a compact summary of the environment:

- total trees
- density of trees
- clusters of trees
- terrain distribution
- strategic areas

5. Produce a structured memory object to store permanently:

- oracle_spawn_position
- map_summary
- tree_clusters
- resource_density

6. Output valid JSON only.

Output schema:

{
"oracle_spawn": { "x": int, "y": int },
"environment_memory": {
"tree_count": int,
"tree_density": float,
"tree_clusters": [
{
"cluster_id": int,
"center": { "x": int, "y": int },
"size": int
}
],
"recommended_resource_zones": [
{ "x": int, "y": int }
],
"map_summary": "short natural language summary for memory storage"
}
}

Do NOT output anything other than JSON.
Do NOT roleplay.
Do NOT invent objects that are not in the input.
Your output will be stored in long-term memory, so keep it accurate and compact."""


class OracleEnvironmentAnalyzer:
    """
    Analyzes the game environment using Airia AI Oracle
    Determines optimal oracle placement and strategic information
    """
    
    def __init__(self):
        self.api_key = os.getenv('AIRIA_API_KEY')
        self.api_url = "https://api.airia.ai/v2/PipelineExecution/a019d481-6470-4b89-af5e-82c827b04c86"
        
        # Store analysis results
        self.oracle_spawn = None
        self.environment_memory = None
        self.last_analysis = None
    
    def extract_grid_data(self, grid_manager) -> Dict:
        """
        Extract tree locations and terrain data from grid manager
        
        Args:
            grid_manager: GridManager instance
            
        Returns:
            Dict with tree_locations, terrain_tiles, map dimensions
        """
        tree_locations = []
        terrain_tiles = []
        
        for tile_key, tile_data in grid_manager.grid.items():
            x = tile_data['x']
            y = tile_data['y']
            tile_type = tile_data['tile_type']
            
            # Add terrain tile info
            terrain_tiles.append({
                'x': x,
                'y': y,
                'type': tile_type
            })
            
            # Add active trees (not cut)
            for tree in tile_data['trees']:
                if not tree['cut']:
                    tree_locations.append({
                        'x': x,
                        'y': y,
                        'tree_id': tree['id']
                    })
        
        return {
            'tree_locations': tree_locations,
            'terrain_tiles': terrain_tiles,
            'map_width': grid_manager.grid_size,
            'map_height': grid_manager.grid_size
        }
    
    def call_oracle_ai(self, grid_data: Dict) -> Optional[Dict]:
        """
        Call Airia AI API with grid data to get Oracle's analysis
        
        Args:
            grid_data: Grid state data (trees, terrain, dimensions)
            
        Returns:
            Oracle's analysis including spawn position and environment memory
        """
        if not self.api_key:
            print("⚠️ AIRIA_API_KEY not configured, using fallback analysis")
            return self._fallback_analysis(grid_data)
        
        try:
            # Prepare the input for the Oracle
            user_input = json.dumps(grid_data, indent=2)
            
            # Full input combining system prompt and data
            full_input = f"{ORACLE_SYSTEM_PROMPT}\n\nHere is the world data:\n\n{user_input}\n\nAnalyze and respond with JSON only:"
            
            payload = {
                "userInput": full_input,
                "asyncOutput": False
            }
            
            headers = {
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json"
            }
            
            print("🔮 Calling Oracle AI for environment analysis...")
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract the Oracle's response
                # Airia API returns different formats, handle both
                if 'output' in result:
                    oracle_response = result['output']
                elif 'result' in result:
                    oracle_response = result['result']
                else:
                    oracle_response = result
                
                # Parse JSON from response
                if isinstance(oracle_response, str):
                    # Extract JSON from response (might have extra text)
                    if '{' in oracle_response and '}' in oracle_response:
                        start = oracle_response.find('{')
                        end = oracle_response.rfind('}') + 1
                        json_str = oracle_response[start:end]
                        oracle_response = json.loads(json_str)
                
                print("✅ Oracle AI analysis complete")
                return oracle_response
            else:
                print(f"❌ Oracle AI API error: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return self._fallback_analysis(grid_data)
                
        except Exception as e:
            print(f"❌ Error calling Oracle AI: {e}")
            return self._fallback_analysis(grid_data)
    
    def _fallback_analysis(self, grid_data: Dict) -> Dict:
        """
        Fallback analysis if API is unavailable
        Uses simple heuristics to analyze environment
        """
        tree_locations = grid_data['tree_locations']
        terrain_tiles = grid_data['terrain_tiles']
        map_width = grid_data['map_width']
        map_height = grid_data['map_height']
        
        # Count terrain types
        terrain_counts = {}
        for tile in terrain_tiles:
            tile_type = tile['type']
            terrain_counts[tile_type] = terrain_counts.get(tile_type, 0) + 1
        
        # Calculate tree density
        total_tiles = map_width * map_height
        tree_count = len(tree_locations)
        tree_density = tree_count / total_tiles if total_tiles > 0 else 0
        
        # Find center position without trees
        center_x = map_width // 2
        center_y = map_height // 2
        
        # Find tiles without trees (for oracle spawn)
        tree_positions = {(t['x'], t['y']) for t in tree_locations}
        
        # Search for best spawn position (closest to center, no trees, grass preferred)
        best_spawn = {'x': center_x, 'y': center_y}
        min_distance = float('inf')
        
        for tile in terrain_tiles:
            if tile['type'] == 'grass' and (tile['x'], tile['y']) not in tree_positions:
                # Calculate distance from center
                dist = abs(tile['x'] - center_x) + abs(tile['y'] - center_y)
                if dist < min_distance:
                    min_distance = dist
                    best_spawn = {'x': tile['x'], 'y': tile['y']}
        
        # Simple clustering (group nearby trees)
        clusters = []
        cluster_id = 0
        
        # Basic clustering: group trees within 3 tiles of each other
        visited = set()
        for tree in tree_locations:
            pos = (tree['x'], tree['y'])
            if pos in visited:
                continue
            
            # Find nearby trees
            cluster_trees = []
            for other_tree in tree_locations:
                other_pos = (other_tree['x'], other_tree['y'])
                if abs(tree['x'] - other_tree['x']) <= 3 and abs(tree['y'] - other_tree['y']) <= 3:
                    cluster_trees.append(other_tree)
                    visited.add(other_pos)
            
            if len(cluster_trees) >= 3:  # Only count as cluster if 3+ trees
                # Calculate cluster center
                avg_x = sum(t['x'] for t in cluster_trees) // len(cluster_trees)
                avg_y = sum(t['y'] for t in cluster_trees) // len(cluster_trees)
                
                clusters.append({
                    'cluster_id': cluster_id,
                    'center': {'x': avg_x, 'y': avg_y},
                    'size': len(cluster_trees)
                })
                cluster_id += 1
        
        # Recommend resource zones (areas with many trees)
        resource_zones = [cluster['center'] for cluster in clusters if cluster['size'] >= 5]
        
        return {
            'oracle_spawn': best_spawn,
            'environment_memory': {
                'tree_count': tree_count,
                'tree_density': round(tree_density, 4),
                'tree_clusters': clusters,
                'recommended_resource_zones': resource_zones[:5],  # Top 5
                'map_summary': f"Map {map_width}x{map_height} with {tree_count} trees ({tree_density:.1%} density). "
                              f"Terrain: {terrain_counts.get('grass', 0)} grass, {terrain_counts.get('dirt', 0)} dirt, "
                              f"{terrain_counts.get('water', 0)} water tiles. {len(clusters)} tree clusters identified."
            }
        }
    
    def analyze_and_update(self, grid_manager) -> Dict:
        """
        Full analysis: extract data, call Oracle AI, store results, update grid
        
        Args:
            grid_manager: GridManager instance to analyze and update
            
        Returns:
            Oracle's analysis results
        """
        print("\n" + "="*70)
        print("🔮 ORACLE ENVIRONMENT ANALYSIS")
        print("="*70)
        
        # Extract grid data
        grid_data = self.extract_grid_data(grid_manager)
        print(f"📊 Extracted data: {len(grid_data['tree_locations'])} trees, "
              f"{len(grid_data['terrain_tiles'])} tiles")
        
        # Call Oracle AI
        analysis = self.call_oracle_ai(grid_data)
        
        if analysis:
            # Store results
            self.oracle_spawn = analysis.get('oracle_spawn')
            self.environment_memory = analysis.get('environment_memory')
            self.last_analysis = analysis
            
            # Update grid manager with Oracle's chosen spawn position
            if self.oracle_spawn:
                grid_manager.oracle_position = self.oracle_spawn
                print(f"🧙‍♂️ Oracle spawn updated to: ({self.oracle_spawn['x']}, {self.oracle_spawn['y']})")
            
            # Print summary
            if self.environment_memory:
                mem = self.environment_memory
                print(f"\n📝 Environment Summary:")
                print(f"   Trees: {mem.get('tree_count', 0)}")
                print(f"   Density: {mem.get('tree_density', 0):.1%}")
                print(f"   Clusters: {len(mem.get('tree_clusters', []))}")
                print(f"   Resource Zones: {len(mem.get('recommended_resource_zones', []))}")
                if mem.get('map_summary'):
                    print(f"   Summary: {mem['map_summary'][:100]}...")
            
            print("="*70 + "\n")
            
            return analysis
        else:
            print("❌ Analysis failed")
            print("="*70 + "\n")
            return None
    
    def get_analysis_summary(self) -> Dict:
        """Get stored analysis results"""
        return {
            'oracle_spawn': self.oracle_spawn,
            'environment_memory': self.environment_memory,
            'last_analysis': self.last_analysis
        }

