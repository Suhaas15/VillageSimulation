"""
Builder AI Agent
Calls Airia AI Builder API and executes actions based on output
"""

import os
import re
import requests
import json
import time
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()

BUILDER_SYSTEM_PROMPT = """You are a Builder agent in an autonomous village simulation game.

You are placed on a 10x10 grid world with trees, grass, dirt, and water tiles.

Your available actions:
1. TALK "message" - Communicate with other agents or log a message
2. WALK x,y - Move to position (x, y) on the grid
3. CUT x,y,tree_id - Cut a tree at position (x, y) with tree_id
4. BUILD type,x,y - Build a structure of 'type' at position (x, y)

You will receive information about:
- Your current position
- Nearby trees and resources
- Current inventory (wood, stone, food)
- Your assigned task

Based on this information, you must decide your next action.

Output ONLY a single action command in one of the formats above.
Examples:
- TALK "I'm starting to gather wood"
- WALK 5,10
- CUT 5,10,42
- BUILD house,12,8

Do NOT output multiple actions.
Do NOT add explanations.
Output ONLY the action command."""


class BuilderAgent:
    """
    Builder AI agent that uses Airia AI to make decisions and execute actions
    """
    
    def __init__(self, grid_manager, agent_id: str = "builder_1"):
        self.api_key = os.getenv('AIRIA_API_KEY')
        self.api_url = "https://api.airia.ai/v2/PipelineExecution/3828632d-7e5a-4a21-a99d-fbcb9a49b1eb"
        
        self.grid_manager = grid_manager
        self.agent_id = agent_id
        
        # Agent state
        self.position = {'x': 0, 'y': 0}
        self.inventory = {'wood': 0, 'stone': 0, 'food': 0}
        self.current_task = None
        self.action_history = []
        
        # Initialize position (random safe location)
        self._initialize_position()
    
    def _initialize_position(self):
        """Initialize builder near the Oracle"""
        oracle_pos = self.grid_manager.oracle_position
        
        if not oracle_pos:
            # No Oracle position yet, use fallback
            self.position = {'x': 1, 'y': 1}
            print(f"🏗️ Builder {self.agent_id} spawned at (1, 1) [no Oracle]")
            return
        
        # Try to spawn adjacent to Oracle (1-2 tiles away)
        for radius in [1, 2, 3]:
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    if dx == 0 and dy == 0:
                        continue
                    
                    x = oracle_pos['x'] + dx
                    y = oracle_pos['y'] + dy
                    
                    # Check if position is valid
                    if 0 <= x < self.grid_manager.grid_size and 0 <= y < self.grid_manager.grid_size:
                        tile_key = f"{x},{y}"
                        tile = self.grid_manager.grid.get(tile_key)
                        
                        if tile and tile['tile_type'] == 'grass':
                            active_trees = [t for t in tile['trees'] if not t['cut']]
                            if len(active_trees) == 0:
                                self.position = {'x': x, 'y': y}
                                distance = abs(dx) + abs(dy)
                                print(f"🏗️ Builder {self.agent_id} spawned at ({x}, {y}) - {distance} tiles from Oracle")
                                return
        
        # Fallback: spawn at Oracle position (shouldn't happen)
        self.position = {'x': oracle_pos['x'], 'y': oracle_pos['y']}
        print(f"🏗️ Builder {self.agent_id} spawned at Oracle position (fallback)")
    
    def get_context(self) -> str:
        """
        Build context string for AI about current state
        """
        # Get current tile
        tile_key = f"{self.position['x']},{self.position['y']}"
        current_tile = self.grid_manager.grid.get(tile_key, {})
        
        # Get nearby tiles (3x3 area around builder)
        nearby_tiles = []
        nearby_trees = []
        
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                x = self.position['x'] + dx
                y = self.position['y'] + dy
                
                if 0 <= x < self.grid_manager.grid_size and 0 <= y < self.grid_manager.grid_size:
                    tile_key = f"{x},{y}"
                    tile = self.grid_manager.grid.get(tile_key)
                    
                    if tile:
                        nearby_tiles.append({
                            'x': x,
                            'y': y,
                            'type': tile['tile_type']
                        })
                        
                        # Check for trees
                        for tree in tile['trees']:
                            if not tree['cut']:
                                nearby_trees.append({
                                    'x': x,
                                    'y': y,
                                    'tree_id': tree['id'],
                                    'type': tree['type']
                                })
        
        # Build context
        context = f"""BUILDER STATUS:
Agent ID: {self.agent_id}
Current Position: ({self.position['x']}, {self.position['y']})
Current Tile Type: {current_tile.get('tile_type', 'unknown')}

INVENTORY:
Wood: {self.inventory['wood']}
Stone: {self.inventory['stone']}
Food: {self.inventory['food']}

NEARBY ENVIRONMENT (3x3 area):
Tiles: {len(nearby_tiles)}
Trees Available: {len(nearby_trees)}
"""
        
        if nearby_trees:
            context += "\nNEARBY TREES:\n"
            for tree in nearby_trees[:5]:  # Show first 5
                context += f"  - {tree['type']} at ({tree['x']}, {tree['y']}) ID: {tree['tree_id']}\n"
        
        if self.current_task:
            context += f"\nCURRENT TASK: {self.current_task}\n"
        
        context += f"\nGRID SIZE: {self.grid_manager.grid_size}x{self.grid_manager.grid_size}\n"
        context += f"\nRESOURCES NEEDED: Wood for building, trees for wood\n"
        
        return context
    
    def call_builder_ai(self, context: str) -> Optional[str]:
        """
        Call Airia AI Builder API to get next action
        
        Args:
            context: Current game state context
            
        Returns:
            Action command string or None if failed
        """
        if not self.api_key:
            print("⚠️ AIRIA_API_KEY not configured, using fallback logic")
            return self._fallback_decision(context)
        
        try:
            # Prepare input
            user_input = f"{BUILDER_SYSTEM_PROMPT}\n\n{context}\n\nWhat is your next action?"
            
            payload = {
                "userInput": user_input,
                "asyncOutput": False
            }
            
            headers = {
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json"
            }
            
            print(f"🤖 Calling Builder AI for {self.agent_id}...")
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract output (Airia returns different formats)
                if isinstance(result, dict):
                    action = result.get('output') or result.get('result') or str(result)
                else:
                    action = str(result)
                
                # Clean up action string
                action = action.strip()
                
                print(f"✅ Builder AI returned: {action}")
                return action
            else:
                print(f"❌ Builder AI API error: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return self._fallback_decision(context)
                
        except Exception as e:
            print(f"❌ Error calling Builder AI: {e}")
            return self._fallback_decision(context)
    
    def _fallback_decision(self, context: str) -> str:
        """
        Fallback decision logic if AI is unavailable
        Simple heuristic-based decision making
        """
        # Check if we have nearby trees and low wood
        if self.inventory['wood'] < 50:
            # Look for nearby trees to cut
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    x = self.position['x'] + dx
                    y = self.position['y'] + dy
                    
                    if 0 <= x < self.grid_manager.grid_size and 0 <= y < self.grid_manager.grid_size:
                        tile_key = f"{x},{y}"
                        tile = self.grid_manager.grid.get(tile_key)
                        
                        if tile:
                            for tree in tile['trees']:
                                if not tree['cut']:
                                    return f"CUT {x},{y},{tree['id']}"
            
            # No nearby trees, move to find some
            return f"WALK {min(self.position['x'] + 2, self.grid_manager.grid_size - 1)},{self.position['y']}"
        
        # Have wood, maybe build something
        if self.inventory['wood'] >= 100:
            # Find a safe spot to build
            build_x = min(self.position['x'] + 1, self.grid_manager.grid_size - 1)
            build_y = self.position['y']
            return f"BUILD house,{build_x},{build_y}"
        
        # Default: talk
        return f'TALK "Gathering resources for the village"'
    
    def parse_and_execute_action(self, action_string: str) -> Dict:
        """
        Parse action string and execute the corresponding action
        
        Args:
            action_string: Action command from AI (e.g., "WALK 5,10")
            
        Returns:
            Result dictionary with success status and details
        """
        action_string = action_string.strip()
        
        # TALK action
        if action_string.startswith('TALK'):
            match = re.search(r'TALK\s+"([^"]+)"', action_string) or re.search(r"TALK\s+'([^']+)'", action_string)
            if match:
                message = match.group(1)
                return self.action_talk(message)
        
        # WALK action
        if action_string.startswith('WALK'):
            match = re.search(r'WALK\s+(\d+),(\d+)', action_string)
            if match:
                x, y = int(match.group(1)), int(match.group(2))
                return self.action_walk(x, y)
        
        # CUT action
        if action_string.startswith('CUT'):
            match = re.search(r'CUT\s+(\d+),(\d+),(\d+)', action_string)
            if match:
                x, y, tree_id = int(match.group(1)), int(match.group(2)), int(match.group(3))
                return self.action_cut(x, y, tree_id)
        
        # BUILD action
        if action_string.startswith('BUILD'):
            match = re.search(r'BUILD\s+(\w+),(\d+),(\d+)', action_string)
            if match:
                building_type, x, y = match.group(1), int(match.group(2)), int(match.group(3))
                return self.action_build(building_type, x, y)
        
        return {
            'success': False,
            'error': f'Invalid action format: {action_string}',
            'action': 'unknown'
        }
    
    # ==================== ACTION IMPLEMENTATIONS ====================
    
    def action_talk(self, message: str) -> Dict:
        """
        TALK action - Log a message
        """
        self.action_history.append({
            'action': 'talk',
            'message': message,
            'position': self.position.copy()
        })
        
        print(f"💬 Builder {self.agent_id}: \"{message}\"")
        
        return {
            'success': True,
            'action': 'talk',
            'message': message
        }
    
    def action_walk(self, x: int, y: int) -> Dict:
        """
        WALK action - Move to position (x, y)
        """
        # Validate position
        if not (0 <= x < self.grid_manager.grid_size and 0 <= y < self.grid_manager.grid_size):
            return {
                'success': False,
                'action': 'walk',
                'error': f'Position ({x}, {y}) out of bounds'
            }
        
        old_pos = self.position.copy()
        self.position = {'x': x, 'y': y}
        
        self.action_history.append({
            'action': 'walk',
            'from': old_pos,
            'to': self.position.copy()
        })
        
        print(f"🚶 Builder {self.agent_id} walked from ({old_pos['x']}, {old_pos['y']}) to ({x}, {y})")
        
        return {
            'success': True,
            'action': 'walk',
            'from': old_pos,
            'to': self.position.copy()
        }
    
    def action_cut(self, x: int, y: int, tree_id: int) -> Dict:
        """
        CUT action - Cut tree at position
        """
        # Check if position is adjacent or same as builder position
        distance = abs(x - self.position['x']) + abs(y - self.position['y'])
        if distance > 1:
            return {
                'success': False,
                'action': 'cut',
                'error': f'Tree at ({x}, {y}) is too far away (distance: {distance})'
            }
        
        # Try to cut the tree
        success, wood_gained = self.grid_manager.cut_tree(x, y, tree_id)
        
        if success:
            self.inventory['wood'] += wood_gained
            
            self.action_history.append({
                'action': 'cut',
                'position': {'x': x, 'y': y},
                'tree_id': tree_id,
                'wood_gained': wood_gained
            })
            
            print(f"🪓 Builder {self.agent_id} cut tree {tree_id} at ({x}, {y}), gained {wood_gained} wood")
            
            return {
                'success': True,
                'action': 'cut',
                'tree_id': tree_id,
                'position': {'x': x, 'y': y},
                'wood_gained': wood_gained,
                'inventory': self.inventory.copy()
            }
        else:
            return {
                'success': False,
                'action': 'cut',
                'error': 'Tree not found or already cut'
            }
    
    def action_build(self, building_type: str, x: int, y: int) -> Dict:
        """
        BUILD action - Build a structure
        """
        # Validate position
        if not (0 <= x < self.grid_manager.grid_size and 0 <= y < self.grid_manager.grid_size):
            return {
                'success': False,
                'action': 'build',
                'error': f'Position ({x}, {y}) out of bounds'
            }
        
        # Check if position is adjacent
        distance = abs(x - self.position['x']) + abs(y - self.position['y'])
        if distance > 2:
            return {
                'success': False,
                'action': 'build',
                'error': f'Build location ({x}, {y}) is too far away'
            }
        
        # Check resource requirements
        requirements = {
            'house': {'wood': 50, 'stone': 20},
            'workshop': {'wood': 100, 'stone': 50},
            'farm': {'wood': 30, 'stone': 10}
        }
        
        if building_type not in requirements:
            return {
                'success': False,
                'action': 'build',
                'error': f'Unknown building type: {building_type}'
            }
        
        required = requirements[building_type]
        
        # Check if builder has enough resources
        if self.inventory['wood'] < required['wood'] or self.inventory['stone'] < required['stone']:
            return {
                'success': False,
                'action': 'build',
                'error': f'Insufficient resources. Need: {required}, Have: {self.inventory}'
            }
        
        # Deduct resources
        self.inventory['wood'] -= required['wood']
        self.inventory['stone'] -= required['stone']
        
        self.action_history.append({
            'action': 'build',
            'building_type': building_type,
            'position': {'x': x, 'y': y},
            'resources_used': required
        })
        
        print(f"🏗️ Builder {self.agent_id} built {building_type} at ({x}, {y})")
        
        return {
            'success': True,
            'action': 'build',
            'building_type': building_type,
            'position': {'x': x, 'y': y},
            'resources_used': required,
            'inventory': self.inventory.copy()
        }
    
    def think_and_act(self) -> Dict:
        """
        Main loop: Get context, call AI, execute action
        
        Returns:
            Result of executed action
        """
        # Get current context
        context = self.get_context()
        
        # Call AI to decide action
        action_string = self.call_builder_ai(context)
        
        if not action_string:
            return {
                'success': False,
                'error': 'No action returned from AI'
            }
        
        # Parse and execute action
        result = self.parse_and_execute_action(action_string)
        result['action_string'] = action_string
        
        return result
    
    def get_state(self) -> Dict:
        """Get builder's current state"""
        return {
            'agent_id': self.agent_id,
            'position': self.position,
            'inventory': self.inventory,
            'current_task': self.current_task,
            'action_count': len(self.action_history),
            'recent_actions': self.action_history[-5:] if self.action_history else []
        }

