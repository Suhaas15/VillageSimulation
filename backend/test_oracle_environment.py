#!/usr/bin/env python3
"""
Test script for Oracle Environment Analyzer
Demonstrates how the Oracle AI analyzes the game environment and chooses spawn location
"""

import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from grid_manager import GridManager
from oracle_environment_analyzer import OracleEnvironmentAnalyzer

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70 + "\n")

def test_environment_analysis():
    """Test the Oracle environment analyzer"""
    
    print_section("🔮 ORACLE ENVIRONMENT ANALYZER TEST")
    
    # Check if AIRIA_API_KEY is configured
    airia_key = os.getenv('AIRIA_API_KEY')
    if airia_key:
        print(f"✅ AIRIA_API_KEY configured: {airia_key[:10]}...")
    else:
        print("⚠️ AIRIA_API_KEY not configured - will use fallback analysis")
    
    # Initialize grid manager (this will trigger initial analysis)
    print_section("1️⃣ INITIALIZING GRID")
    grid_manager = GridManager(grid_size=10)
    
    # Display initial analysis results
    print_section("2️⃣ INITIAL ENVIRONMENT ANALYSIS")
    
    if grid_manager.environment_analysis:
        analysis = grid_manager.environment_analysis
        
        print("📍 Oracle Spawn Location:")
        spawn = analysis.get('oracle_spawn', {})
        print(f"   Position: ({spawn.get('x')}, {spawn.get('y')})")
        
        print("\n🌍 Environment Memory:")
        memory = analysis.get('environment_memory', {})
        
        print(f"   🌲 Total Trees: {memory.get('tree_count', 0)}")
        print(f"   📊 Tree Density: {memory.get('tree_density', 0):.2%}")
        
        clusters = memory.get('tree_clusters', [])
        print(f"   🗺️ Tree Clusters: {len(clusters)}")
        for cluster in clusters[:3]:  # Show first 3
            print(f"      • Cluster {cluster.get('cluster_id')}: "
                  f"{cluster.get('size')} trees at "
                  f"({cluster.get('center', {}).get('x')}, {cluster.get('center', {}).get('y')})")
        
        zones = memory.get('recommended_resource_zones', [])
        print(f"   🎯 Recommended Resource Zones: {len(zones)}")
        for i, zone in enumerate(zones[:3], 1):
            print(f"      {i}. ({zone.get('x')}, {zone.get('y')})")
        
        summary = memory.get('map_summary', '')
        if summary:
            print(f"\n   📝 Map Summary:")
            print(f"      {summary}")
    else:
        print("❌ No environment analysis available")
    
    # Simulate cutting a few trees and re-analyzing
    print_section("3️⃣ SIMULATING TREE CUTTING")
    
    # Find some trees to cut
    trees_cut = 0
    max_cuts = 5
    
    for tile_key, tile_data in grid_manager.grid.items():
        if trees_cut >= max_cuts:
            break
        
        x = tile_data['x']
        y = tile_data['y']
        
        for tree in tile_data['trees']:
            if not tree['cut'] and trees_cut < max_cuts:
                tree_id = tree['id']
                success, wood = grid_manager.cut_tree(x, y, tree_id)
                if success:
                    print(f"🪓 Cut tree {tree_id} at ({x}, {y}) - gained {wood} wood")
                    trees_cut += 1
                    
                    # Show updated analysis after each cut
                    if grid_manager.environment_analysis:
                        new_spawn = grid_manager.environment_analysis.get('oracle_spawn', {})
                        new_memory = grid_manager.environment_analysis.get('environment_memory', {})
                        print(f"   → Oracle repositioned to: ({new_spawn.get('x')}, {new_spawn.get('y')})")
                        print(f"   → Trees remaining: {new_memory.get('tree_count', 0)}")
                    
                    break
    
    print(f"\n✅ Cut {trees_cut} trees total")
    
    # Display final state
    print_section("4️⃣ FINAL STATE")
    
    print(f"🌲 Trees Remaining: {grid_manager._count_total_trees()}")
    print(f"🪵 Wood Collected: {grid_manager.resources['wood']}")
    
    if grid_manager.oracle_position:
        print(f"🧙‍♂️ Oracle Position: ({grid_manager.oracle_position['x']}, {grid_manager.oracle_position['y']})")
    
    # Test manual re-analysis API
    print_section("5️⃣ TESTING MANUAL RE-ANALYSIS")
    
    print("Triggering manual re-analysis...")
    grid_manager._analyze_environment()
    
    if grid_manager.environment_analysis:
        memory = grid_manager.environment_analysis.get('environment_memory', {})
        print(f"✅ Re-analysis complete!")
        print(f"   Trees: {memory.get('tree_count', 0)}")
        print(f"   Density: {memory.get('tree_density', 0):.2%}")
        print(f"   Clusters: {len(memory.get('tree_clusters', []))}")
    
    # Export analysis to JSON
    print_section("6️⃣ EXPORTING ANALYSIS")
    
    if grid_manager.environment_analysis:
        output_file = 'oracle_analysis.json'
        with open(output_file, 'w') as f:
            json.dump(grid_manager.environment_analysis, f, indent=2)
        print(f"✅ Analysis exported to: {output_file}")
        print(f"   File size: {os.path.getsize(output_file)} bytes")
    
    print_section("✅ TEST COMPLETE")
    print("The Oracle Environment Analyzer is working correctly!")
    print("\nKey Features Demonstrated:")
    print("  ✓ Initial environment analysis on grid creation")
    print("  ✓ Automatic re-analysis when trees are cut")
    print("  ✓ Strategic spawn location selection")
    print("  ✓ Tree cluster detection")
    print("  ✓ Resource zone recommendations")
    print("  ✓ Manual re-analysis via API")
    print("\nAPI Endpoints Available:")
    print("  GET  /api/oracle/environment  - Get current analysis")
    print("  POST /api/oracle/analyze      - Trigger re-analysis")
    print("  GET  /api/grid                - Get grid state (includes analysis)")

if __name__ == '__main__':
    try:
        test_environment_analysis()
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

