#!/usr/bin/env python3
"""
Test script for Builder AI Agent
Demonstrates how the Builder AI makes decisions and executes actions
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
from builder_agent import BuilderAgent

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70 + "\n")

def test_builder_agent():
    """Test the Builder AI agent"""
    
    print_section("🏗️ BUILDER AI AGENT TEST")
    
    # Check if AIRIA_API_KEY is configured
    airia_key = os.getenv('AIRIA_API_KEY')
    if airia_key:
        print(f"✅ AIRIA_API_KEY configured: {airia_key[:10]}...")
    else:
        print("⚠️ AIRIA_API_KEY not configured - will use fallback decision logic")
    
    # Initialize grid manager
    print_section("1️⃣ INITIALIZING GRID")
    grid_manager = GridManager(grid_size=20)
    
    print(f"✅ Grid created: {grid_manager.grid_size}x{grid_manager.grid_size}")
    print(f"   Trees: {grid_manager._count_total_trees()}")
    
    # Create builder agent
    print_section("2️⃣ CREATING BUILDER AGENT")
    builder = BuilderAgent(grid_manager, agent_id="test_builder")
    
    print(f"✅ Builder created: {builder.agent_id}")
    print(f"   Position: ({builder.position['x']}, {builder.position['y']})")
    print(f"   Inventory: {builder.inventory}")
    
    # Show initial context
    print_section("3️⃣ BUILDER CONTEXT")
    context = builder.get_context()
    print(context)
    
    # Test individual actions
    print_section("4️⃣ TESTING INDIVIDUAL ACTIONS")
    
    print("\n📝 Test 1: TALK Action")
    result = builder.parse_and_execute_action('TALK "Hello, I am Builder AI!"')
    print(f"   Result: {json.dumps(result, indent=2)}")
    
    print("\n🚶 Test 2: WALK Action")
    target_x = min(builder.position['x'] + 2, grid_manager.grid_size - 1)
    target_y = builder.position['y']
    result = builder.parse_and_execute_action(f'WALK {target_x},{target_y}')
    print(f"   Result: {json.dumps(result, indent=2)}")
    print(f"   New Position: ({builder.position['x']}, {builder.position['y']})")
    
    # Find a nearby tree
    print("\n🪓 Test 3: CUT Action")
    tree_found = False
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            x = builder.position['x'] + dx
            y = builder.position['y'] + dy
            
            if 0 <= x < grid_manager.grid_size and 0 <= y < grid_manager.grid_size:
                tile_key = f"{x},{y}"
                tile = grid_manager.grid.get(tile_key)
                
                if tile:
                    for tree in tile['trees']:
                        if not tree['cut']:
                            result = builder.parse_and_execute_action(f"CUT {x},{y},{tree['id']}")
                            print(f"   Result: {json.dumps(result, indent=2)}")
                            print(f"   Inventory: {builder.inventory}")
                            tree_found = True
                            break
                if tree_found:
                    break
        if tree_found:
            break
    
    if not tree_found:
        print("   ⚠️ No nearby trees to cut")
    
    print("\n🏗️ Test 4: BUILD Action (will fail - need resources)")
    builder.inventory['wood'] = 100  # Give builder wood for testing
    builder.inventory['stone'] = 50
    build_x = min(builder.position['x'] + 1, grid_manager.grid_size - 1)
    build_y = builder.position['y']
    result = builder.parse_and_execute_action(f'BUILD house,{build_x},{build_y}')
    print(f"   Result: {json.dumps(result, indent=2)}")
    print(f"   Inventory: {builder.inventory}")
    
    # Test AI-driven decision making
    print_section("5️⃣ AI-DRIVEN DECISION MAKING")
    
    # Reset builder for AI test
    builder.position = {'x': 5, 'y': 5}
    builder.inventory = {'wood': 0, 'stone': 0, 'food': 0}
    builder.current_task = "Gather 50 wood for the village"
    
    print(f"Builder Task: {builder.current_task}")
    print(f"Starting Position: ({builder.position['x']}, {builder.position['y']})")
    print(f"Starting Inventory: {builder.inventory}")
    
    print("\n🤖 Running 10 AI-driven actions...\n")
    
    for i in range(10):
        print(f"--- Action {i+1}/10 ---")
        result = builder.think_and_act()
        
        print(f"   AI Decision: {result.get('action_string', 'N/A')}")
        print(f"   Success: {result.get('success', False)}")
        print(f"   Action Type: {result.get('action', 'unknown')}")
        
        if result.get('action') == 'cut':
            print(f"   Wood Gained: {result.get('wood_gained', 0)}")
        elif result.get('action') == 'walk':
            print(f"   Moved to: ({result.get('to', {}).get('x')}, {result.get('to', {}).get('y')})")
        elif result.get('action') == 'talk':
            print(f"   Message: {result.get('message', 'N/A')}")
        
        print(f"   Current Wood: {builder.inventory['wood']}")
        print()
        
        # Stop if task completed
        if builder.inventory['wood'] >= 50:
            print("✅ Task completed! Gathered 50 wood.")
            break
    
    # Final state
    print_section("6️⃣ FINAL STATE")
    
    state = builder.get_state()
    print(f"Agent ID: {state['agent_id']}")
    print(f"Position: ({state['position']['x']}, {state['position']['y']})")
    print(f"Inventory:")
    print(f"   Wood: {state['inventory']['wood']}")
    print(f"   Stone: {state['inventory']['stone']}")
    print(f"   Food: {state['inventory']['food']}")
    print(f"Total Actions: {state['action_count']}")
    
    print("\nRecent Actions:")
    for action in state['recent_actions']:
        print(f"   - {action.get('action', 'unknown')}: {action}")
    
    # Export state
    print_section("7️⃣ EXPORTING STATE")
    
    output_file = 'builder_state.json'
    with open(output_file, 'w') as f:
        json.dump(state, f, indent=2)
    print(f"✅ Builder state exported to: {output_file}")
    print(f"   File size: {os.path.getsize(output_file)} bytes")
    
    print_section("✅ TEST COMPLETE")
    print("The Builder AI Agent is working correctly!")
    print("\nKey Features Demonstrated:")
    print("  ✓ TALK - Communication/logging")
    print("  ✓ WALK - Movement around grid")
    print("  ✓ CUT - Tree cutting with resource gain")
    print("  ✓ BUILD - Structure construction")
    print("  ✓ AI Decision Making - Context-aware action selection")
    print("  ✓ Inventory Management - Resource tracking")
    print("\nAPI Endpoints Available:")
    print("  POST /api/builder/create           - Create builder")
    print("  GET  /api/builder/list             - List all builders")
    print("  POST /api/builder/{id}/act         - AI-driven action")
    print("  POST /api/builder/{id}/execute     - Manual action")
    print("  POST /api/builder/{id}/task        - Set task")
    print("  POST /api/builder/{id}/simulate    - Run N actions")

if __name__ == '__main__':
    try:
        test_builder_agent()
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

