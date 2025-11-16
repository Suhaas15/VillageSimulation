import random
import json
from typing import List, Dict, Tuple, Optional
try:
    from oracle_environment_analyzer import OracleEnvironmentAnalyzer
    ORACLE_ANALYZER_AVAILABLE = True
except ImportError:
    ORACLE_ANALYZER_AVAILABLE = False
    print("⚠️ Oracle Environment Analyzer not available")

class GridManager:
    """Manages the 40x40 grid state, tree placement, and resources"""
    
    def __init__(self, grid_size: int = 40):
        self.grid_size = grid_size
        self.grid: Dict[str, Dict] = {}
        self.resources = {
            'wood': 0,
            'stone': 0,
            'food': 0
        }
        self.tree_id_counter = 0
        self.oracle_position = None  # Will store oracle's grid position
        self.oracle_analyzer = OracleEnvironmentAnalyzer() if ORACLE_ANALYZER_AVAILABLE else None
        self.environment_analysis = None  # Store Oracle AI's analysis
        
    def _get_tile_key(self, x: int, y: int) -> str:
        """Generate unique key for tile position"""
        return f"{x},{y}"
    
    def initialize_grid(self):
        """Initialize the grid with default tiles and random trees"""
        print(f"Generating {self.grid_size}x{self.grid_size} grid...")
        
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                tile_key = self._get_tile_key(x, y)
                
                # Determine tile type (mostly grass, some dirt/water)
                tile_type = self._random_tile_type()
                
                # Create tile
                self.grid[tile_key] = {
                    'x': x,
                    'y': y,
                    'tile_type': tile_type,
                    'tile_image_url': None,  # Will be populated by Freepik
                    'trees': self._generate_trees_for_tile(x, y, tile_type)
                }
        
        print(f"✅ Grid initialized with {self._count_total_trees()} trees")
        
        # Analyze environment with Oracle AI and determine spawn location
        self._analyze_environment()
    
    def _random_tile_type(self) -> str:
        """Randomly select tile type with weighted probability"""
        rand = random.random()
        if rand < 0.75:
            return 'grass'
        elif rand < 0.90:
            return 'dirt'
        else:
            return 'water'
    
    def _generate_trees_for_tile(self, x: int, y: int, tile_type: str) -> List[Dict]:
        """Generate 1-2 random trees per tile (except water)"""
        trees = []
        
        # Don't place trees on water
        if tile_type == 'water':
            return trees
        
        # 70% chance of having trees on grass/dirt
        if random.random() < 0.7:
            num_trees = random.randint(1, 2)
        else:
            num_trees = 0
        
        for _ in range(num_trees):
            tree = {
                'id': self._get_next_tree_id(),
                'position': {
                    # Random position within the tile (0-100% offsets)
                    'offset_x': random.uniform(0.1, 0.9),
                    'offset_y': random.uniform(0.1, 0.9)
                },
                'cut': False,
                'type': random.choice(['oak', 'pine', 'birch'])
            }
            trees.append(tree)
        
        return trees
    
    def _get_next_tree_id(self) -> int:
        """Get next unique tree ID"""
        tree_id = self.tree_id_counter
        self.tree_id_counter += 1
        return tree_id
    
    def _count_total_trees(self) -> int:
        """Count total trees in grid"""
        count = 0
        for tile in self.grid.values():
            count += len([t for t in tile['trees'] if not t['cut']])
        return count
    
    def _analyze_environment(self):
        """
        Analyze environment using Oracle AI
        Determines optimal spawn location and stores strategic information
        """
        if self.oracle_analyzer:
            try:
                # Call Oracle AI to analyze environment
                analysis = self.oracle_analyzer.analyze_and_update(self)
                if analysis:
                    self.environment_analysis = analysis
                    # Oracle position is already set by analyzer
                    return
            except Exception as e:
                print(f"❌ Oracle analysis failed: {e}")
        
        # Fallback to simple spawn logic
        self._spawn_oracle_fallback()
    
    def _spawn_oracle_fallback(self):
        """
        Fallback: Spawn oracle at a random valid location (no AI)
        Valid location = grass tile with no trees
        """
        valid_positions = []
        
        # Find all grass tiles without trees
        for tile_key, tile_data in self.grid.items():
            if tile_data['tile_type'] == 'grass':
                # Check if tile has no trees (or all trees are cut)
                active_trees = [t for t in tile_data['trees'] if not t['cut']]
                if len(active_trees) == 0:
                    valid_positions.append({
                        'x': tile_data['x'],
                        'y': tile_data['y']
                    })
        
        # Choose random position from valid ones
        if valid_positions:
            oracle_pos = random.choice(valid_positions)
            self.oracle_position = oracle_pos
            print(f"🧙‍♂️ Oracle spawned at ({oracle_pos['x']}, {oracle_pos['y']}) [fallback]")
        else:
            # Fallback: spawn at center if no valid positions
            self.oracle_position = {'x': self.grid_size // 2, 'y': self.grid_size // 2}
            print(f"⚠️ No valid positions, Oracle spawned at center ({self.oracle_position['x']}, {self.oracle_position['y']})")
    
    def get_grid_state(self) -> Dict:
        """Get complete grid state"""
        return {
            'grid_size': self.grid_size,
            'tiles': list(self.grid.values()),
            'resources': self.resources,
            'oracle_position': self.oracle_position,  # Include oracle position
            'environment_analysis': self.environment_analysis,  # Include Oracle AI analysis
            'stats': {
                'total_trees': self._count_total_trees(),
                'trees_cut': self.tree_id_counter - self._count_total_trees()
            }
        }
    
    def get_viewport(self, x_start: int, y_start: int, x_end: int, y_end: int) -> Dict:
        """Get a viewport slice of the grid for rendering optimization"""
        viewport_tiles = []
        
        for x in range(x_start, min(x_end, self.grid_size)):
            for y in range(y_start, min(y_end, self.grid_size)):
                tile_key = self._get_tile_key(x, y)
                if tile_key in self.grid:
                    viewport_tiles.append(self.grid[tile_key])
        
        return {
            'viewport': {
                'x_start': x_start,
                'y_start': y_start,
                'x_end': x_end,
                'y_end': y_end
            },
            'tiles': viewport_tiles,
            'resources': self.resources
        }
    
    def cut_tree(self, x: int, y: int, tree_id: int) -> Tuple[bool, int]:
        """
        Cut down a tree and gain resources
        Returns (success, wood_gained)
        """
        tile_key = self._get_tile_key(x, y)
        
        if tile_key not in self.grid:
            return False, 0
        
        tile = self.grid[tile_key]
        
        # Find the tree
        for tree in tile['trees']:
            if tree['id'] == tree_id and not tree['cut']:
                tree['cut'] = True
                wood_gained = random.randint(5, 15)  # Random wood per tree
                self.resources['wood'] += wood_gained
                print(f"🪓 Tree {tree_id} cut at ({x}, {y}). Gained {wood_gained} wood.")
                
                # Trigger environment re-analysis (tree landscape changed)
                self._analyze_environment()
                
                return True, wood_gained
        
        return False, 0
    
    def get_resources(self) -> Dict:
        """Get current resource counts"""
        return self.resources.copy()
    
    def reset_grid(self):
        """Reset grid to initial state"""
        self.grid = {}
        self.resources = {
            'wood': 0,
            'stone': 0,
            'food': 0
        }
        self.tree_id_counter = 0
        self.initialize_grid()
    
    def initialize_with_freepik(self, freepik_api):
        """Initialize grid and fetch tile images from Freepik"""
        print("🎨 Generating tiles with Freepik API...")
        
        # Generate tile images for each type
        tile_types = ['grass', 'dirt', 'forest', 'water']
        tile_images = {}
        
        for tile_type in tile_types:
            # Generate 3-5 variations per tile type
            urls = freepik_api.generate_tiles(tile_type, count=5)
            tile_images[tile_type] = urls
        
        # Assign images to tiles
        for tile in self.grid.values():
            tile_type = tile['tile_type']
            if tile_type in tile_images and tile_images[tile_type]:
                tile['tile_image_url'] = random.choice(tile_images[tile_type])
        
        print("✅ Tiles assigned with Freepik images")
    
    def apply_tile_images(self, tile_images_dict):
        """
        Apply generated tile images to the grid
        
        Args:
            tile_images_dict: Dictionary with tile_type as key and image URL as value
                             e.g. {'grass': 'data:image/...', 'dirt': 'data:image/...'}
        """
        print(f"🎨 Applying {len(tile_images_dict)} tile images to grid...")
        
        updated_count = 0
        for tile_key, tile_data in self.grid.items():
            tile_type = tile_data.get('tile_type')
            if tile_type in tile_images_dict:
                tile_data['tile_image_url'] = tile_images_dict[tile_type]
                updated_count += 1
        
        print(f"✅ Applied tile images to {updated_count} tiles")
        return updated_count

