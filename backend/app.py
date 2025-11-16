from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
from grid_manager import GridManager
from freepik_api import FreepikAPI

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize grid manager and Freepik API
grid_manager = GridManager(grid_size=10)
freepik_api = FreepikAPI(api_key=os.getenv('FREEPIK_API_KEY', 'your_api_key_here'))

# Import and register village Oracle blueprint
try:
    from village_api import village_bp
    app.register_blueprint(village_bp)
    print("✅ Village Oracle System loaded")
except ImportError as e:
    print(f"⚠️ Village Oracle System not available: {e}")

# Import and register Builder AI blueprint
try:
    from builder_api import builder_bp
    app.register_blueprint(builder_bp)
    print("✅ Builder AI System loaded")
except ImportError as e:
    print(f"⚠️ Builder AI System not available: {e}")

print(f"🔑 Freepik API Key configured: {'Yes' if os.getenv('FREEPIK_API_KEY') and os.getenv('FREEPIK_API_KEY') != 'your_api_key_here' else 'No (using placeholders)'}")
print(f"🔑 OpenAI API Key configured: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No (using fallback logic)'}")
print(f"🔑 Airia API Key configured: {'Yes' if os.getenv('AIRIA_API_KEY') else 'No (Builder will use fallback)'}")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'village-backend'})

@app.route('/api/grid', methods=['GET'])
def get_grid():
    """Get the entire grid state"""
    grid_data = grid_manager.get_grid_state()
    return jsonify(grid_data)

@app.route('/api/grid/viewport', methods=['GET'])
def get_viewport():
    """Get a specific viewport of the grid for optimization"""
    x_start = int(request.args.get('x_start', 0))
    y_start = int(request.args.get('y_start', 0))
    x_end = int(request.args.get('x_end', 40))
    y_end = int(request.args.get('y_end', 40))
    
    viewport_data = grid_manager.get_viewport(x_start, y_start, x_end, y_end)
    return jsonify(viewport_data)

@app.route('/api/tree/cut', methods=['POST'])
def cut_tree():
    """Cut down a tree at specified tile and tree_id"""
    data = request.json
    x = data.get('x')
    y = data.get('y')
    tree_id = data.get('tree_id')
    
    if x is None or y is None or tree_id is None:
        return jsonify({'success': False, 'error': 'Missing x, y, or tree_id'}), 400
    
    success, wood_gained = grid_manager.cut_tree(x, y, tree_id)
    
    if success:
        return jsonify({
            'success': True,
            'wood_gained': wood_gained,
            'total_resources': grid_manager.get_resources()
        }), 200
    else:
        # Return 200 with success: false instead of 404
        # This prevents browser errors and is better for UX
        return jsonify({
            'success': False, 
            'error': 'Tree not found or already cut',
            'wood_gained': 0
        }), 200

@app.route('/api/resources', methods=['GET'])
def get_resources():
    """Get global resource counts"""
    return jsonify(grid_manager.get_resources())

@app.route('/api/grid/stats', methods=['GET'])
def get_grid_stats():
    """Get statistics about tile types in the grid"""
    tile_counts = {}
    for tile_key, tile_data in grid_manager.grid.items():
        tile_type = tile_data.get('tile_type', 'unknown')
        tile_counts[tile_type] = tile_counts.get(tile_type, 0) + 1
    
    return jsonify({
        'total_tiles': len(grid_manager.grid),
        'tile_counts': tile_counts,
        'grid_size': grid_manager.grid_size
    })

@app.route('/api/oracle/environment', methods=['GET'])
def get_oracle_environment():
    """Get Oracle's current environment analysis"""
    if grid_manager.environment_analysis:
        return jsonify({
            'success': True,
            'analysis': grid_manager.environment_analysis
        })
    else:
        return jsonify({
            'success': False,
            'message': 'No environment analysis available yet'
        })

@app.route('/api/oracle/analyze', methods=['POST'])
def trigger_oracle_analysis():
    """Manually trigger Oracle environment analysis"""
    try:
        grid_manager._analyze_environment()
        
        if grid_manager.environment_analysis:
            return jsonify({
                'success': True,
                'message': 'Environment analysis completed',
                'analysis': grid_manager.environment_analysis
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Analysis failed or Oracle not available'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tiles/generate', methods=['POST'])
def generate_tiles():
    """Generate tile images using Freepik API"""
    data = request.json
    tile_type = data.get('tile_type', 'grass')
    count = data.get('count', 1)
    
    # Generate tiles using Freepik
    tile_urls = freepik_api.generate_tiles(tile_type, count)
    
    return jsonify({
        'tile_type': tile_type,
        'tiles': tile_urls
    })

@app.route('/api/grid/initialize', methods=['POST'])
def initialize_grid():
    """Initialize grid with generated tiles from Freepik"""
    grid_manager.initialize_with_freepik(freepik_api)
    return jsonify({
        'success': True,
        'message': 'Grid initialized with Freepik tiles',
        'grid_size': grid_manager.grid_size
    })

@app.route('/api/grid/reset', methods=['POST'])
def reset_grid():
    """Reset the grid to initial state"""
    grid_manager.reset_grid()
    return jsonify({
        'success': True,
        'message': 'Grid reset complete'
    })

@app.route('/api/assets/generate', methods=['POST'])
def generate_environment_assets():
    """
    Generate all environment assets using Freepik API and apply them to grid
    - 5 tile types (grass, dirt, stone, forest, water)
    """
    try:
        # Generate all tile assets
        assets = freepik_api.generate_environment_assets()
        
        # Apply generated tiles to the grid
        tiles_updated = 0
        if assets.get('tiles'):
            tiles_updated = grid_manager.apply_tile_images(assets['tiles'])
        
        return jsonify({
            'success': True,
            'assets': assets,
            'tiles_updated': tiles_updated,
            'summary': {
                'trees_generated': len(assets.get('trees', [])),
                'tiles_generated': len(assets.get('tiles', {})),
                'grid_tiles_updated': tiles_updated
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/assets/generate/trees', methods=['POST'])
def generate_tree_sprites():
    """Generate 3 tree sprites with background removal"""
    try:
        trees = freepik_api.generate_tree_sprites()
        
        return jsonify({
            'success': True,
            'trees': trees,
            'count': len(trees)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/assets/generate/tile', methods=['POST'])
def generate_single_tile():
    """Generate a single tile type and apply it to the grid"""
    data = request.json
    tile_type = data.get('tile_type', 'grass')
    
    try:
        # Generate the tile using Freepik
        tile_urls = freepik_api.generate_tiles(tile_type, count=1)
        tile_url = tile_urls[0] if tile_urls else None
        
        if tile_url:
            # Apply this tile to all tiles of this type in the grid
            updated_count = grid_manager.apply_tile_images({tile_type: tile_url})
            
            return jsonify({
                'success': True,
                'tile_type': tile_type,
                'url': tile_url,
                'tiles_updated': updated_count
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to generate tile image'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/assets/generate/tiles/all', methods=['POST'])
def generate_all_tiles():
    """Generate all 5 tile types and apply them to the grid"""
    try:
        # Generate tile images using Freepik
        print("🎨 Starting tile generation and application...")
        tiles = freepik_api.generate_all_tiles()
        
        # Apply generated tiles to the grid
        updated_count = grid_manager.apply_tile_images(tiles)
        
        return jsonify({
            'success': True,
            'tiles': tiles,
            'count': len(tiles),
            'tiles_updated': updated_count,
            'message': f'Generated {len(tiles)} tile types and applied to {updated_count} grid tiles'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Initialize grid on startup
    print("🌳 Initializing Village Grid...")
    grid_manager.initialize_grid()
    print(f"✅ Grid initialized: {grid_manager.grid_size}x{grid_manager.grid_size}")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
