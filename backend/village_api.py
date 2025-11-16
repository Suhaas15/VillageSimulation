"""
Village Oracle API Endpoints
Flask endpoints for the autonomous village simulation
"""

from flask import Blueprint, jsonify, request
from village_state import VillageState
from oracle_agent import OracleAgent
import os

# Create blueprint
village_bp = Blueprint('village', __name__, url_prefix='/api/village')

# Initialize village state and oracle
village_state = VillageState()
oracle_agent = OracleAgent(api_key=os.getenv('OPENAI_API_KEY'))

# Store simulation state
simulation_running = False


@village_bp.route('/state', methods=['GET'])
def get_village_state():
    """
    Get current village state
    
    Returns:
        JSON with complete village state
    """
    return jsonify({
        'success': True,
        'state': village_state.get_state_for_oracle(),
        'summary': village_state.get_summary()
    })


@village_bp.route('/oracle/consult', methods=['POST'])
def consult_oracle():
    """
    Consult the Oracle AI for decisions
    
    Agents can call this endpoint to get Oracle's decisions for current state
    
    Returns:
        Oracle's decisions in JSON format
    """
    try:
        # Get current state
        current_state = village_state.get_state_for_oracle()
        
        # Get Oracle's decisions
        decisions = oracle_agent.make_decision(current_state)
        
        return jsonify({
            'success': True,
            'decisions': decisions,
            'day': village_state.day
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@village_bp.route('/oracle/apply', methods=['POST'])
def apply_oracle_decisions():
    """
    Apply Oracle's decisions to the village
    
    Request body should contain Oracle's decision JSON
    """
    try:
        decisions = request.json
        
        if not decisions:
            return jsonify({
                'success': False,
                'error': 'No decisions provided'
            }), 400
        
        # Apply decisions
        messages = village_state.apply_oracle_decisions(decisions)
        
        return jsonify({
            'success': True,
            'messages': messages,
            'updated_state': village_state.get_state_for_oracle()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@village_bp.route('/day/execute', methods=['POST'])
def execute_day():
    """
    Execute one day of simulation
    All villagers perform their assigned tasks
    
    Returns:
        Action results and updated state
    """
    try:
        messages = village_state.execute_day()
        
        return jsonify({
            'success': True,
            'day': village_state.day - 1,  # Just completed this day
            'messages': messages,
            'state': village_state.get_state_for_oracle()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@village_bp.route('/cycle', methods=['POST'])
def run_oracle_cycle():
    """
    Run a complete Oracle cycle:
    1. Consult Oracle for decisions
    2. Apply decisions
    3. Execute day
    
    This is the main autonomous loop
    """
    try:
        results = {
            'day': village_state.day,
            'oracle_decisions': None,
            'apply_messages': [],
            'execution_messages': [],
            'final_state': None
        }
        
        # Step 1: Consult Oracle
        print(f"\n🔮 Consulting Oracle for Day {village_state.day}...")
        current_state = village_state.get_state_for_oracle()
        decisions = oracle_agent.make_decision(current_state)
        results['oracle_decisions'] = decisions
        
        # Step 2: Apply Oracle's decisions
        print("📋 Applying Oracle's decisions...")
        apply_messages = village_state.apply_oracle_decisions(decisions)
        results['apply_messages'] = apply_messages
        
        # Step 3: Execute the day
        print("⚡ Executing day...")
        execution_messages = village_state.execute_day()
        results['execution_messages'] = execution_messages
        
        # Get final state
        results['final_state'] = village_state.get_state_for_oracle()
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'day': village_state.day
        }), 500


@village_bp.route('/simulate', methods=['POST'])
def simulate_days():
    """
    Simulate multiple days of autonomous operation
    
    Request body:
    {
      "days": 10  // Number of days to simulate
    }
    """
    try:
        data = request.json or {}
        days = data.get('days', 1)
        
        if days < 1 or days > 100:
            return jsonify({
                'success': False,
                'error': 'Days must be between 1 and 100'
            }), 400
        
        all_results = []
        
        for i in range(days):
            print(f"\n{'='*60}")
            print(f"SIMULATING DAY {village_state.day}")
            print(f"{'='*60}")
            
            # Run Oracle cycle
            current_state = village_state.get_state_for_oracle()
            decisions = oracle_agent.make_decision(current_state)
            apply_messages = village_state.apply_oracle_decisions(decisions)
            execution_messages = village_state.execute_day()
            
            day_result = {
                'day': village_state.day - 1,
                'decisions': decisions,
                'execution_summary': execution_messages[-2:]  # Last 2 messages (resource summary)
            }
            all_results.append(day_result)
        
        return jsonify({
            'success': True,
            'days_simulated': days,
            'results': all_results,
            'final_state': village_state.get_state_for_oracle(),
            'summary': village_state.get_summary()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@village_bp.route('/reset', methods=['POST'])
def reset_village():
    """Reset village to initial state"""
    global village_state
    village_state = VillageState()
    
    return jsonify({
        'success': True,
        'message': 'Village reset to initial state',
        'state': village_state.get_state_for_oracle()
    })


@village_bp.route('/villager/add', methods=['POST'])
def add_villager():
    """
    Add a new villager
    
    Request body:
    {
      "name": "David",
      "job": "woodcutter",
      "job_tier": 1
    }
    """
    try:
        data = request.json
        name = data.get('name')
        job = data.get('job', 'woodcutter')
        tier = data.get('job_tier', 1)
        
        if not name:
            return jsonify({
                'success': False,
                'error': 'Name required'
            }), 400
        
        village_state.add_villager(name, job, tier)
        
        return jsonify({
            'success': True,
            'message': f'Added villager {name} as {job} (T{tier})',
            'state': village_state.get_state_for_oracle()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@village_bp.route('/resources/add', methods=['POST'])
def add_resources():
    """
    Add resources to village (admin/cheat)
    
    Request body:
    {
      "wood": 100,
      "food": 50,
      "stone": 30
    }
    """
    try:
        data = request.json
        
        for resource, amount in data.items():
            if resource in village_state.resources:
                village_state.resources[resource] += amount
        
        return jsonify({
            'success': True,
            'resources': village_state.resources
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

