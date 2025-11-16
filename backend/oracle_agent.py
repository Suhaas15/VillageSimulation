"""
Oracle Agent Integration
Handles communication with AI agent (OpenAI, Claude, etc.) to make village decisions
"""

import os
import json
from typing import Dict, Optional
import openai
from dotenv import load_dotenv

load_dotenv()

# Oracle system prompt (from your specification)
ORACLE_SYSTEM_PROMPT = """
You are The Oracle, the supreme AI governor of an autonomous village simulation.

Your job is to make perfectly rational, strategic, resource-based decisions for the village.

The user does NOT interact. Only you decide the future of the village.

You MUST output only valid JSON matching the required schema.

🧱 JOB TREES (3 tiers per villager)

🌲 Wood path
1️⃣ Woodcutter (tier 1 → gathers wood)
2️⃣ Lumberjack (tier 2 → gathers more efficiently)
3️⃣ Builder (tier 3 → can construct buildings)

🌾 Food path
1️⃣ Forager (tier 1 → basic food gathering)
2️⃣ Farmer (tier 2 → stable food production)
3️⃣ Chef (tier 3 → food boosts)

⛏ Stone path
1️⃣ Miner (tier 1 → basic stone gathering)
2️⃣ Excavator (tier 2 → fast mining)
3️⃣ Engineer (tier 3 → supports builders, boosts construction speed)

🏗 TASK TYPES
"chop_wood", "gather_food", "mine_stone", "cook_food", "farm_crops", "build_house", "build_workshop", "build_farm", "rest"

🧠 ORACLE DECISION LOGIC

1️⃣ Resource Management Rules
If wood < 100: Prioritize wood tasks (all woodcutters → chop_wood)
If food < 100: Prioritize food tasks (foragers → gather_food, farmers → farm_crops)
If stone < 80: Prioritize mining tasks (all miners → mine_stone)

2️⃣ Building Construction Rules
When wood ≥ 200: Assign one builder to "build_house"
When stone ≥ 150 AND wood ≥ 100: Assign engineer to "build_workshop"
When food ≥ 180: Assign farmer/chef to "build_farm"

3️⃣ Promotion Rules
Wood Path: Woodcutter → Lumberjack (exp > 70), Lumberjack → Builder (wood > 200, exp > 85)
Food Path: Forager → Farmer (exp > 70), Farmer → Chef (food > 200, exp > 90)
Stone Path: Miner → Excavator (exp > 70), Excavator → Engineer (stone > 150, exp > 90)

4️⃣ Task Assignment Rules
After promotions, assign tasks based on tier and resource needs.
If stamina < 0.2 → assign "rest" no matter what.

🧾 OUTPUT FORMAT (MUST FOLLOW EXACTLY)

Output ONLY this JSON structure:
{
  "assignments": [
    {
      "name": "villager_name",
      "new_job": "same_or_promoted_job",
      "job_tier": 1|2|3,
      "task": "string"
    }
  ],
  "build_actions": [
    {
      "building": "house|workshop|farm",
      "assigned_to": "villager_name"
    }
  ]
}

No text. No explanations. JSON only.
"""


class OracleAgent:
    """
    Oracle AI Agent that makes decisions for the village
    Can use OpenAI, Claude, or any other LLM
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize Oracle agent
        
        Args:
            api_key: OpenAI API key (or None to use env var)
            model: Model to use (gpt-4, gpt-3.5-turbo, etc.)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        
        if self.api_key:
            openai.api_key = self.api_key
        
        self.system_prompt = ORACLE_SYSTEM_PROMPT
    
    def make_decision(self, village_state: Dict) -> Dict:
        """
        Send village state to Oracle AI and get decisions
        
        Args:
            village_state: Current village state (resources, villagers, buildings, day)
            
        Returns:
            Oracle's decisions in JSON format
        """
        if not self.api_key:
            print("⚠️ No OpenAI API key configured, using fallback logic")
            return self._fallback_logic(village_state)
        
        try:
            # Format state as JSON for the prompt
            state_json = json.dumps(village_state, indent=2)
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Current village state:\n\n{state_json}\n\nMake your decisions:"}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse response
            content = response.choices[0].message.content.strip()
            
            # Extract JSON (in case AI added explanation)
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            decisions = json.loads(content)
            
            return decisions
            
        except json.JSONDecodeError as e:
            print(f"❌ Oracle returned invalid JSON: {e}")
            print(f"Response was: {content[:200]}")
            return self._fallback_logic(village_state)
        except Exception as e:
            print(f"❌ Oracle error: {e}")
            return self._fallback_logic(village_state)
    
    def _fallback_logic(self, state: Dict) -> Dict:
        """
        Simple rule-based fallback logic when AI is unavailable
        Implements the same rules as the Oracle prompt
        """
        resources = state['resources']
        villagers = state['villagers']
        
        assignments = []
        build_actions = []
        
        for villager in villagers:
            name = villager['name']
            job = villager['job']
            tier = villager['job_tier']
            exp = villager['experience']
            stamina = villager['stamina']
            
            # Check for rest
            if stamina < 0.2:
                assignments.append({
                    'name': name,
                    'new_job': job,
                    'job_tier': tier,
                    'task': 'rest'
                })
                continue
            
            # Check for promotions
            new_job, new_tier = self._check_promotion(job, tier, exp, resources)
            
            # Assign task based on resource needs
            task = self._assign_task(new_job, new_tier, resources)
            
            assignments.append({
                'name': name,
                'new_job': new_job,
                'job_tier': new_tier,
                'task': task
            })
            
            # Check if we should build something
            if new_tier == 3 and task.startswith('build_'):
                building_type = task.replace('build_', '')
                build_actions.append({
                    'building': building_type,
                    'assigned_to': name
                })
        
        return {
            'assignments': assignments,
            'build_actions': build_actions
        }
    
    def _check_promotion(self, job: str, tier: int, exp: int, resources: Dict) -> tuple:
        """Check if villager should be promoted"""
        # Wood path
        if job == 'woodcutter' and tier == 1 and exp > 70:
            return 'lumberjack', 2
        if job == 'lumberjack' and tier == 2 and exp > 85 and resources['wood'] > 200:
            return 'builder', 3
        
        # Food path
        if job == 'forager' and tier == 1 and exp > 70:
            return 'farmer', 2
        if job == 'farmer' and tier == 2 and exp > 90 and resources['food'] > 200:
            return 'chef', 3
        
        # Stone path
        if job == 'miner' and tier == 1 and exp > 70:
            return 'excavator', 2
        if job == 'excavator' and tier == 2 and exp > 90 and resources['stone'] > 150:
            return 'engineer', 3
        
        return job, tier
    
    def _assign_task(self, job: str, tier: int, resources: Dict) -> str:
        """Assign task based on job and resource needs"""
        wood = resources['wood']
        food = resources['food']
        stone = resources['stone']
        
        # Tier 3 (specialized jobs)
        if tier == 3:
            if job == 'builder' and wood >= 200:
                return 'build_house'
            elif job == 'engineer' and stone >= 150 and wood >= 100:
                return 'build_workshop'
            elif job == 'chef' and food >= 180:
                if food > 50:  # Need raw food to cook
                    return 'cook_food'
                else:
                    return 'gather_food'
        
        # Resource priorities
        if wood < 100 and job in ['woodcutter', 'lumberjack', 'builder']:
            return 'chop_wood'
        
        if food < 100:
            if job == 'forager':
                return 'gather_food'
            elif job in ['farmer', 'chef']:
                return 'farm_crops'
        
        if stone < 80 and job in ['miner', 'excavator', 'engineer']:
            return 'mine_stone'
        
        # Default tasks by job
        task_map = {
            'woodcutter': 'chop_wood',
            'lumberjack': 'chop_wood',
            'builder': 'chop_wood',
            'forager': 'gather_food',
            'farmer': 'farm_crops',
            'chef': 'cook_food',
            'miner': 'mine_stone',
            'excavator': 'mine_stone',
            'engineer': 'mine_stone'
        }
        
        return task_map.get(job, 'rest')

