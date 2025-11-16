"""
Builder-Oracle Orchestration System
Coordinates between Oracle (strategic) and Builder AI (tactical) for autonomous decisions
"""

import os
import requests
import json
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

ORACLE_STRATEGIC_PROMPT = """You are the Oracle, the strategic decision-maker for Builder agents in a village simulation.

A Builder has consulted you for guidance on what they should do next.

Builder Information:
{builder_context}

Your role is to provide HIGH-LEVEL strategic guidance based on:
- Village needs (resources, buildings, expansion)
- Builder's current state and capabilities
- Optimal resource allocation
- Priority tasks for village growth

Output ONLY a strategic directive in this format:
DIRECTIVE: <strategic_goal>

Examples:
- DIRECTIVE: Gather wood from the northern forest cluster
- DIRECTIVE: Build a house near the village center
- DIRECTIVE: Explore the eastern region for resources
- DIRECTIVE: Rest and maintain your tools
- DIRECTIVE: Collect stone from the mountain area

Do NOT output specific coordinates or detailed steps.
Do NOT output multiple directives.
Output ONLY the strategic directive."""


class BuilderOracleOrchestrator:
    """
    Orchestrates the Builder-Oracle-Action workflow:
    1. Builder consults Oracle for strategic decision
    2. Oracle provides high-level directive
    3. Builder AI converts directive to specific action
    4. Action is executed
    """
    
    def __init__(self):
        self.api_key = os.getenv('AIRIA_API_KEY')
        self.oracle_api_url = "https://api.airia.ai/v2/PipelineExecution/31a5bde8-9c32-4038-9fa0-f347df23aa52"
        self.builder_api_url = "https://api.airia.ai/v2/PipelineExecution/3828632d-7e5a-4a21-a99d-fbcb9a49b1eb"
    
    def consult_oracle(self, builder_context: str) -> Optional[str]:
        """
        Step 1: Consult Oracle for strategic directive
        
        Args:
            builder_context: Current builder state and environment
            
        Returns:
            Strategic directive string or None if failed
        """
        if not self.api_key:
            print("⚠️ AIRIA_API_KEY not configured, using fallback")
            return self._oracle_fallback(builder_context)
        
        try:
            # Format prompt with builder context
            user_input = ORACLE_STRATEGIC_PROMPT.format(builder_context=builder_context)
            
            payload = {
                "userInput": user_input,
                "asyncOutput": False
            }
            
            headers = {
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json"
            }
            
            print("🔮 Consulting Oracle for strategic guidance...")
            response = requests.post(self.oracle_api_url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract directive
                if isinstance(result, dict):
                    directive = result.get('output') or result.get('result') or str(result)
                else:
                    directive = str(result)
                
                directive = directive.strip()
                
                # Extract just the directive text
                if "DIRECTIVE:" in directive:
                    directive = directive.split("DIRECTIVE:")[1].strip()
                
                print(f"✅ Oracle says: {directive}")
                return directive
            else:
                print(f"❌ Oracle API error: {response.status_code}")
                return self._oracle_fallback(builder_context)
                
        except Exception as e:
            print(f"❌ Error consulting Oracle: {e}")
            return self._oracle_fallback(builder_context)
    
    def _oracle_fallback(self, builder_context: str) -> str:
        """Fallback strategic logic if Oracle API unavailable"""
        if "wood: 0" in builder_context.lower() or "wood: " in builder_context.lower():
            # Check inventory
            try:
                wood_val = int(builder_context.split("wood: ")[1].split()[0])
                if wood_val < 50:
                    return "Gather wood from nearby trees"
            except:
                pass
        
        if "trees available: 0" in builder_context.lower():
            return "Explore and find resource-rich areas"
        
        if "stone: 0" in builder_context.lower() or "stone: " in builder_context.lower():
            try:
                stone_val = int(builder_context.split("stone: ")[1].split()[0])
                if stone_val > 50:
                    return "Build structures for the village"
            except:
                pass
        
        return "Gather resources for village development"
    
    def get_tactical_action(self, directive: str, builder_context: str) -> Optional[str]:
        """
        Step 2: Convert Oracle directive to specific Builder action
        
        Args:
            directive: Strategic directive from Oracle
            builder_context: Current builder state
            
        Returns:
            Tactical action command (WALK/CUT/BUILD/TALK) or None if failed
        """
        if not self.api_key:
            print("⚠️ AIRIA_API_KEY not configured, using fallback")
            return self._builder_fallback(directive, builder_context)
        
        try:
            # Format prompt for Builder AI
            user_input = f"""You are a Builder agent. The Oracle has given you this directive:
"{directive}"

Your current state:
{builder_context}

Based on the Oracle's directive and your current state, output your NEXT SPECIFIC ACTION.

Available actions:
- TALK "message" - Communicate or log
- WALK x,y - Move to coordinates
- CUT x,y,tree_id - Cut a tree
- BUILD type,x,y - Build structure (house/workshop/farm)

Output ONLY ONE action command. No explanations."""
            
            payload = {
                "userInput": user_input,
                "asyncOutput": False
            }
            
            headers = {
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json"
            }
            
            print("🤖 Builder AI converting directive to action...")
            response = requests.post(self.builder_api_url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract action
                if isinstance(result, dict):
                    action = result.get('output') or result.get('result') or str(result)
                else:
                    action = str(result)
                
                action = action.strip()
                print(f"✅ Builder AI action: {action}")
                return action
            else:
                print(f"❌ Builder AI API error: {response.status_code}")
                return self._builder_fallback(directive, builder_context)
                
        except Exception as e:
            print(f"❌ Error getting tactical action: {e}")
            return self._builder_fallback(directive, builder_context)
    
    def _builder_fallback(self, directive: str, builder_context: str) -> str:
        """Fallback tactical logic if Builder API unavailable"""
        directive_lower = directive.lower()
        
        # Parse directive and context to determine action
        if "wood" in directive_lower or "gather" in directive_lower or "tree" in directive_lower:
            # Look for tree in context
            if "tree" in builder_context.lower() and "id:" in builder_context.lower():
                try:
                    # Try to extract tree info
                    lines = builder_context.split('\n')
                    for line in lines:
                        if 'tree' in line.lower() and 'id:' in line.lower():
                            # Parse coordinates and ID
                            return 'TALK "Looking for trees to cut"'
                except:
                    pass
            return 'TALK "I will gather wood as the Oracle commands"'
        
        elif "build" in directive_lower:
            return 'TALK "Preparing to build as the Oracle commands"'
        
        elif "explore" in directive_lower:
            return 'TALK "I will explore as the Oracle commands"'
        
        elif "rest" in directive_lower:
            return 'TALK "Resting as the Oracle advises"'
        
        else:
            return f'TALK "Acknowledged: {directive}"'
    
    def orchestrate_builder_action(self, builder_agent) -> Dict:
        """
        Complete orchestration workflow:
        1. Get builder context
        2. Consult Oracle for strategic directive
        3. Get tactical action from Builder AI
        4. Execute action
        
        Args:
            builder_agent: BuilderAgent instance
            
        Returns:
            Result dict with oracle_directive, action_command, and execution_result
        """
        print("\n" + "="*70)
        print("🎭 BUILDER-ORACLE ORCHESTRATION")
        print("="*70)
        
        # Step 1: Get builder context
        context = builder_agent.get_context()
        print("\n📋 Builder Context:")
        print(context[:300] + "..." if len(context) > 300 else context)
        
        # Step 2: Consult Oracle
        print("\n🔮 Step 1: Consulting Oracle...")
        directive = self.consult_oracle(context)
        
        if not directive:
            return {
                'success': False,
                'error': 'Failed to get Oracle directive'
            }
        
        # Step 3: Get tactical action
        print(f"\n🤖 Step 2: Converting directive to action...")
        print(f"   Oracle Directive: \"{directive}\"")
        action_command = self.get_tactical_action(directive, context)
        
        if not action_command:
            return {
                'success': False,
                'error': 'Failed to get tactical action',
                'oracle_directive': directive
            }
        
        # Step 4: Execute action
        print(f"\n⚡ Step 3: Executing action...")
        print(f"   Action Command: {action_command}")
        execution_result = builder_agent.parse_and_execute_action(action_command)
        
        print("\n" + "="*70)
        
        return {
            'success': True,
            'oracle_directive': directive,
            'action_command': action_command,
            'execution_result': execution_result
        }

