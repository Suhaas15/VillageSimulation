"""
Village Actions System
Defines all actions that villagers can perform and their effects
"""

from typing import Dict, Tuple, Optional
import random

class VillageActions:
    """Handles all village actions and their resource/experience effects"""
    
    # Action definitions with their effects
    ACTIONS = {
        # Wood gathering actions
        'chop_wood': {
            'resource': 'wood',
            'base_yield': 10,
            'stamina_cost': 0.15,
            'experience_gain': 5,
            'job_requirements': ['woodcutter', 'lumberjack', 'builder']
        },
        
        # Food gathering actions
        'gather_food': {
            'resource': 'food',
            'base_yield': 8,
            'stamina_cost': 0.12,
            'experience_gain': 5,
            'job_requirements': ['forager', 'farmer', 'chef']
        },
        'farm_crops': {
            'resource': 'food',
            'base_yield': 15,
            'stamina_cost': 0.18,
            'experience_gain': 8,
            'job_requirements': ['farmer', 'chef']
        },
        'cook_food': {
            'resource': 'food',
            'base_yield': 20,
            'stamina_cost': 0.10,
            'experience_gain': 10,
            'job_requirements': ['chef'],
            'requires_resources': {'food': 10}  # Consumes raw food to make more
        },
        
        # Stone gathering actions
        'mine_stone': {
            'resource': 'stone',
            'base_yield': 12,
            'stamina_cost': 0.20,
            'experience_gain': 6,
            'job_requirements': ['miner', 'excavator', 'engineer']
        },
        
        # Building actions
        'build_house': {
            'building': 'houses',
            'resource_cost': {'wood': 50, 'stone': 30},
            'stamina_cost': 0.25,
            'experience_gain': 15,
            'job_requirements': ['builder', 'engineer'],
            'duration': 1  # Takes 1 day to complete
        },
        'build_workshop': {
            'building': 'workshops',
            'resource_cost': {'wood': 80, 'stone': 60},
            'stamina_cost': 0.30,
            'experience_gain': 20,
            'job_requirements': ['builder', 'engineer'],
            'duration': 2
        },
        'build_farm': {
            'building': 'farms',
            'resource_cost': {'wood': 40, 'food': 20},
            'stamina_cost': 0.20,
            'experience_gain': 15,
            'job_requirements': ['farmer', 'chef', 'builder'],
            'duration': 1
        },
        
        # Recovery action
        'rest': {
            'stamina_gain': 0.40,
            'experience_gain': 0,
            'job_requirements': []  # Anyone can rest
        }
    }
    
    # Job tier multipliers for efficiency
    TIER_MULTIPLIERS = {
        1: 1.0,   # Base tier
        2: 1.5,   # 50% more efficient
        3: 2.0    # 100% more efficient (double)
    }
    
    def __init__(self):
        """Initialize action handler"""
        pass
    
    def execute_action(
        self, 
        action: str, 
        villager: Dict, 
        resources: Dict[str, int],
        buildings: Dict[str, int]
    ) -> Tuple[Dict, Dict, Dict, str]:
        """
        Execute a villager action and return updated state
        
        Args:
            action: Action name (e.g., 'chop_wood')
            villager: Villager dict with name, job, job_tier, stamina, experience
            resources: Current resource counts
            buildings: Current building counts
            
        Returns:
            Tuple of (updated_villager, updated_resources, updated_buildings, message)
        """
        if action not in self.ACTIONS:
            return villager, resources, buildings, f"❌ Unknown action: {action}"
        
        action_def = self.ACTIONS[action]
        
        # Check job requirements
        if action_def['job_requirements'] and villager['job'] not in action_def['job_requirements']:
            return villager, resources, buildings, f"❌ {villager['name']} cannot perform {action} (wrong job)"
        
        # Check stamina
        stamina_cost = action_def.get('stamina_cost', 0)
        if villager['stamina'] < stamina_cost:
            return villager, resources, buildings, f"⚠️ {villager['name']} too tired for {action}"
        
        # Execute specific action type
        if action == 'rest':
            return self._execute_rest(villager, resources, buildings, action_def)
        elif 'resource' in action_def:
            return self._execute_resource_gathering(action, villager, resources, buildings, action_def)
        elif 'building' in action_def:
            return self._execute_building(action, villager, resources, buildings, action_def)
        
        return villager, resources, buildings, f"⚠️ Action {action} not implemented"
    
    def _execute_rest(
        self, 
        villager: Dict, 
        resources: Dict, 
        buildings: Dict, 
        action_def: Dict
    ) -> Tuple[Dict, Dict, Dict, str]:
        """Handle rest action"""
        villager = villager.copy()
        stamina_gain = action_def['stamina_gain']
        
        villager['stamina'] = min(1.0, villager['stamina'] + stamina_gain)
        
        return villager, resources, buildings, f"💤 {villager['name']} rested (stamina: {villager['stamina']:.1%})"
    
    def _execute_resource_gathering(
        self, 
        action: str,
        villager: Dict, 
        resources: Dict, 
        buildings: Dict, 
        action_def: Dict
    ) -> Tuple[Dict, Dict, Dict, str]:
        """Handle resource gathering actions"""
        villager = villager.copy()
        resources = resources.copy()
        
        # Check resource requirements (e.g., cooking needs raw food)
        if 'requires_resources' in action_def:
            for res, amount in action_def['requires_resources'].items():
                if resources.get(res, 0) < amount:
                    return villager, resources, buildings, f"⚠️ Not enough {res} for {action}"
            
            # Consume required resources
            for res, amount in action_def['requires_resources'].items():
                resources[res] -= amount
        
        # Calculate yield based on tier
        base_yield = action_def['base_yield']
        tier_multiplier = self.TIER_MULTIPLIERS.get(villager['job_tier'], 1.0)
        
        # Add some randomness (±20%)
        variance = random.uniform(0.8, 1.2)
        actual_yield = int(base_yield * tier_multiplier * variance)
        
        # Add to resources
        resource_type = action_def['resource']
        resources[resource_type] = resources.get(resource_type, 0) + actual_yield
        
        # Update villager state
        villager['stamina'] = max(0, villager['stamina'] - action_def['stamina_cost'])
        villager['experience'] = min(100, villager['experience'] + action_def['experience_gain'])
        
        return (
            villager, 
            resources, 
            buildings,
            f"✅ {villager['name']} +{actual_yield} {resource_type} (stamina: {villager['stamina']:.1%}, exp: {villager['experience']})"
        )
    
    def _execute_building(
        self, 
        action: str,
        villager: Dict, 
        resources: Dict, 
        buildings: Dict, 
        action_def: Dict
    ) -> Tuple[Dict, Dict, Dict, str]:
        """Handle building construction actions"""
        villager = villager.copy()
        resources = resources.copy()
        buildings = buildings.copy()
        
        # Check if we have enough resources
        resource_cost = action_def['resource_cost']
        for res, cost in resource_cost.items():
            if resources.get(res, 0) < cost:
                return villager, resources, buildings, f"⚠️ Not enough {res} to {action}"
        
        # Deduct resources
        for res, cost in resource_cost.items():
            resources[res] -= cost
        
        # Add building
        building_type = action_def['building']
        buildings[building_type] = buildings.get(building_type, 0) + 1
        
        # Update villager state
        villager['stamina'] = max(0, villager['stamina'] - action_def['stamina_cost'])
        villager['experience'] = min(100, villager['experience'] + action_def['experience_gain'])
        
        return (
            villager,
            resources,
            buildings,
            f"🏗️ {villager['name']} built {building_type} (stamina: {villager['stamina']:.1%}, exp: {villager['experience']})"
        )
    
    def can_execute(self, action: str, villager: Dict, resources: Dict) -> Tuple[bool, str]:
        """
        Check if a villager can execute an action
        
        Returns:
            Tuple of (can_execute: bool, reason: str)
        """
        if action not in self.ACTIONS:
            return False, f"Unknown action: {action}"
        
        action_def = self.ACTIONS[action]
        
        # Check job requirements
        if action_def['job_requirements'] and villager['job'] not in action_def['job_requirements']:
            return False, f"Wrong job (need {action_def['job_requirements']})"
        
        # Check stamina
        stamina_cost = action_def.get('stamina_cost', 0)
        if villager['stamina'] < stamina_cost:
            return False, f"Not enough stamina ({villager['stamina']:.1%} < {stamina_cost:.1%})"
        
        # Check resource requirements
        if 'requires_resources' in action_def:
            for res, amount in action_def['requires_resources'].items():
                if resources.get(res, 0) < amount:
                    return False, f"Not enough {res} (need {amount})"
        
        # Check building costs
        if 'resource_cost' in action_def:
            for res, cost in action_def['resource_cost'].items():
                if resources.get(res, 0) < cost:
                    return False, f"Not enough {res} for construction (need {cost})"
        
        return True, "OK"

