"""
Village State Manager
Manages the entire village simulation state
"""

from typing import Dict, List, Optional
import json
from village_actions import VillageActions

class VillageState:
    """Manages village state including villagers, resources, and buildings"""
    
    # Job progression trees
    JOB_TREES = {
        'wood': [
            {'name': 'woodcutter', 'tier': 1},
            {'name': 'lumberjack', 'tier': 2},
            {'name': 'builder', 'tier': 3}
        ],
        'food': [
            {'name': 'forager', 'tier': 1},
            {'name': 'farmer', 'tier': 2},
            {'name': 'chef', 'tier': 3}
        ],
        'stone': [
            {'name': 'miner', 'tier': 1},
            {'name': 'excavator', 'tier': 2},
            {'name': 'engineer', 'tier': 3}
        ]
    }
    
    def __init__(self):
        """Initialize village state"""
        self.resources = {
            'wood': 50,
            'food': 50,
            'stone': 20
        }
        
        self.villagers = [
            {
                'name': 'Alice',
                'job': 'woodcutter',
                'job_tier': 1,
                'stamina': 1.0,
                'experience': 0,
                'assigned_task': None
            },
            {
                'name': 'Bob',
                'job': 'forager',
                'job_tier': 1,
                'stamina': 1.0,
                'experience': 0,
                'assigned_task': None
            },
            {
                'name': 'Charlie',
                'job': 'miner',
                'job_tier': 1,
                'stamina': 1.0,
                'experience': 0,
                'assigned_task': None
            }
        ]
        
        self.buildings = {
            'houses': 1,
            'workshops': 0,
            'farms': 0
        }
        
        self.day = 1
        self.actions_handler = VillageActions()
        self.action_log = []
    
    def get_state_for_oracle(self) -> Dict:
        """
        Get current state formatted for Oracle AI agent
        
        Returns:
            Dict matching Oracle's expected input format
        """
        return {
            'resources': self.resources.copy(),
            'villagers': [v.copy() for v in self.villagers],
            'buildings': self.buildings.copy(),
            'day': self.day
        }
    
    def apply_oracle_decisions(self, decisions: Dict) -> List[str]:
        """
        Apply Oracle's decisions to the village state
        
        Args:
            decisions: Oracle's JSON output with assignments and build_actions
            
        Returns:
            List of action result messages
        """
        messages = []
        
        # Apply job changes and task assignments
        if 'assignments' in decisions:
            for assignment in decisions['assignments']:
                villager_name = assignment.get('name')
                new_job = assignment.get('new_job')
                new_tier = assignment.get('job_tier')
                task = assignment.get('task')
                
                # Find villager
                villager = self._find_villager(villager_name)
                if not villager:
                    messages.append(f"❌ Villager not found: {villager_name}")
                    continue
                
                # Apply job change/promotion
                if new_job and new_job != villager['job']:
                    old_job = villager['job']
                    villager['job'] = new_job
                    villager['job_tier'] = new_tier
                    messages.append(f"⬆️ {villager_name}: {old_job} (T{villager['job_tier']}) → {new_job} (T{new_tier})")
                
                # Assign task
                if task:
                    villager['assigned_task'] = task
        
        # Handle build actions specifically
        if 'build_actions' in decisions:
            for build_action in decisions['build_actions']:
                building = build_action.get('building')
                assigned_to = build_action.get('assigned_to')
                
                villager = self._find_villager(assigned_to)
                if villager:
                    task_name = f"build_{building}"
                    villager['assigned_task'] = task_name
                    messages.append(f"🏗️ {assigned_to} assigned to build {building}")
        
        return messages
    
    def execute_day(self) -> List[str]:
        """
        Execute one day of village simulation
        - All villagers perform their assigned tasks
        - Resources are gathered/consumed
        - Buildings are constructed
        - Experience is gained
        
        Returns:
            List of action result messages
        """
        messages = [f"\n{'='*60}", f"DAY {self.day}", f"{'='*60}\n"]
        
        # Execute each villager's task
        for villager in self.villagers:
            task = villager.get('assigned_task')
            
            if not task:
                messages.append(f"⚠️ {villager['name']} has no assigned task (idle)")
                continue
            
            # Execute the action
            updated_villager, updated_resources, updated_buildings, message = \
                self.actions_handler.execute_action(
                    task,
                    villager,
                    self.resources,
                    self.buildings
                )
            
            # Update state
            villager.update(updated_villager)
            self.resources.update(updated_resources)
            self.buildings.update(updated_buildings)
            
            messages.append(message)
        
        # Increment day
        self.day += 1
        
        # Add resource summary
        messages.append(f"\n📊 RESOURCES: Wood={self.resources['wood']}, Food={self.resources['food']}, Stone={self.resources['stone']}")
        messages.append(f"🏘️ BUILDINGS: Houses={self.buildings['houses']}, Workshops={self.buildings['workshops']}, Farms={self.buildings['farms']}\n")
        
        return messages
    
    def promote_villager(self, villager_name: str, new_job: str, new_tier: int) -> bool:
        """
        Promote a villager to a new job tier
        
        Returns:
            True if successful, False otherwise
        """
        villager = self._find_villager(villager_name)
        if not villager:
            return False
        
        old_job = villager['job']
        old_tier = villager['job_tier']
        
        villager['job'] = new_job
        villager['job_tier'] = new_tier
        
        print(f"⬆️ {villager_name} promoted: {old_job} (T{old_tier}) → {new_job} (T{new_tier})")
        return True
    
    def _find_villager(self, name: str) -> Optional[Dict]:
        """Find villager by name"""
        for villager in self.villagers:
            if villager['name'] == name:
                return villager
        return None
    
    def add_villager(self, name: str, job: str, job_tier: int = 1):
        """Add a new villager to the village"""
        self.villagers.append({
            'name': name,
            'job': job,
            'job_tier': job_tier,
            'stamina': 1.0,
            'experience': 0,
            'assigned_task': None
        })
    
    def get_summary(self) -> str:
        """Get human-readable village summary"""
        lines = [
            f"\n{'='*60}",
            f"VILLAGE STATUS - DAY {self.day}",
            f"{'='*60}",
            f"\n📊 RESOURCES:",
            f"   Wood: {self.resources['wood']}",
            f"   Food: {self.resources['food']}",
            f"   Stone: {self.resources['stone']}",
            f"\n🏘️ BUILDINGS:",
            f"   Houses: {self.buildings['houses']}",
            f"   Workshops: {self.buildings['workshops']}",
            f"   Farms: {self.buildings['farms']}",
            f"\n👥 VILLAGERS ({len(self.villagers)}):"
        ]
        
        for v in self.villagers:
            lines.append(
                f"   {v['name']}: {v['job']} (T{v['job_tier']}) | "
                f"Stamina: {v['stamina']:.1%} | Exp: {v['experience']} | "
                f"Task: {v.get('assigned_task', 'None')}"
            )
        
        lines.append(f"\n{'='*60}\n")
        
        return '\n'.join(lines)

