"""
Builder Agent API Routes
Flask blueprint for Builder AI agent endpoints
"""

from flask import Blueprint, jsonify, request
from builder_agent import BuilderAgent
from builder_oracle_orchestrator import BuilderOracleOrchestrator

builder_bp = Blueprint('builder', __name__, url_prefix='/api/builder')

# Global builder instances (keyed by agent_id)
builders = {}

# Global orchestrator instance
orchestrator = BuilderOracleOrchestrator()

def get_or_create_builder(agent_id: str, grid_manager) -> BuilderAgent:
    """Get existing builder or create new one"""
    if agent_id not in builders:
        builders[agent_id] = BuilderAgent(grid_manager, agent_id=agent_id)
    return builders[agent_id]


@builder_bp.route('/create', methods=['POST'])
def create_builder():
    """
    Create a new builder agent
    
    POST /api/builder/create
    Body: { "agent_id": "builder_1" }
    """
    from app import grid_manager  # Import here to avoid circular dependency
    
    data = request.json or {}
    agent_id = data.get('agent_id', f'builder_{len(builders) + 1}')
    
    if agent_id in builders:
        return jsonify({
            'success': False,
            'error': f'Builder {agent_id} already exists'
        }), 400
    
    builder = BuilderAgent(grid_manager, agent_id=agent_id)
    builders[agent_id] = builder
    
    return jsonify({
        'success': True,
        'agent_id': agent_id,
        'state': builder.get_state()
    })


@builder_bp.route('/list', methods=['GET'])
def list_builders():
    """
    List all active builders
    
    GET /api/builder/list
    """
    return jsonify({
        'success': True,
        'count': len(builders),
        'builders': [builder.get_state() for builder in builders.values()]
    })


@builder_bp.route('/<agent_id>/state', methods=['GET'])
def get_builder_state(agent_id: str):
    """
    Get builder's current state
    
    GET /api/builder/{agent_id}/state
    """
    if agent_id not in builders:
        return jsonify({
            'success': False,
            'error': f'Builder {agent_id} not found'
        }), 404
    
    builder = builders[agent_id]
    return jsonify({
        'success': True,
        'state': builder.get_state()
    })


@builder_bp.route('/<agent_id>/act', methods=['POST'])
def builder_act(agent_id: str):
    """
    Make builder think and execute one action using Builder AI only
    
    POST /api/builder/{agent_id}/act
    """
    from app import grid_manager
    
    builder = get_or_create_builder(agent_id, grid_manager)
    
    # Let builder think and act (direct Builder AI)
    result = builder.think_and_act()
    
    return jsonify({
        'success': result.get('success', False),
        'agent_id': agent_id,
        'result': result,
        'state': builder.get_state()
    })


@builder_bp.route('/<agent_id>/oracle_act', methods=['POST'])
def builder_oracle_act(agent_id: str):
    """
    Make builder consult Oracle, then execute action (Full orchestration)
    
    POST /api/builder/{agent_id}/oracle_act
    Body: { "delay": 5 } (optional, defaults to 0)
    
    Flow:
    1. Builder state → Oracle Strategic AI
    2. Oracle returns strategic directive
    3. Directive + Builder state → Builder Tactical AI
    4. Builder AI returns action command
    5. Action is executed
    """
    import time
    from app import grid_manager
    
    builder = get_or_create_builder(agent_id, grid_manager)
    
    data = request.json or {}
    delay = int(data.get('delay', 0))  # Optional delay before action
    
    # Full orchestration: Oracle → Builder AI → Action
    result = orchestrator.orchestrate_builder_action(builder)
    
    # Apply delay if specified
    if delay > 0 and result.get('success'):
        print(f"⏳ Waiting {delay} seconds after Oracle consultation...")
        time.sleep(delay)
    
    return jsonify({
        'success': result.get('success', False),
        'agent_id': agent_id,
        'oracle_directive': result.get('oracle_directive'),
        'action_command': result.get('action_command'),
        'execution_result': result.get('execution_result'),
        'state': builder.get_state()
    })


@builder_bp.route('/<agent_id>/oracle_simulate', methods=['POST'])
def builder_oracle_simulate(agent_id: str):
    """
    Run builder with Oracle consultation for N steps with 5-second delay
    
    POST /api/builder/{agent_id}/oracle_simulate
    Body: { "steps": 5, "delay": 5 }
    """
    import time
    from app import grid_manager
    
    builder = get_or_create_builder(agent_id, grid_manager)
    
    data = request.json or {}
    steps = int(data.get('steps', 5))
    delay = int(data.get('delay', 5))  # Default 5 seconds
    steps = min(steps, 20)  # Max 20 steps (Oracle calls are slower)
    
    results = []
    
    for i in range(steps):
        print(f"\n⏱️ Oracle Step {i+1}/{steps}...")
        
        # Full orchestration for each step
        result = orchestrator.orchestrate_builder_action(builder)
        results.append({
            'step': i + 1,
            'oracle_directive': result.get('oracle_directive'),
            'action_command': result.get('action_command'),
            'execution_result': result.get('execution_result'),
            'success': result.get('success', False)
        })
        
        # Stop if action failed
        if not result.get('success', False):
            break
        
        # Wait between Oracle consultations (except after last one)
        if i < steps - 1:
            print(f"⏳ Waiting {delay} seconds before next Oracle consultation...")
            time.sleep(delay)
    
    return jsonify({
        'success': True,
        'agent_id': agent_id,
        'steps_executed': len(results),
        'results': results,
        'final_state': builder.get_state()
    })


@builder_bp.route('/<agent_id>/execute', methods=['POST'])
def builder_execute_action(agent_id: str):
    """
    Manually execute a specific action
    
    POST /api/builder/{agent_id}/execute
    Body: { "action": "WALK 5,10" }
    """
    from app import grid_manager
    
    builder = get_or_create_builder(agent_id, grid_manager)
    
    data = request.json or {}
    action_string = data.get('action')
    
    if not action_string:
        return jsonify({
            'success': False,
            'error': 'No action provided'
        }), 400
    
    result = builder.parse_and_execute_action(action_string)
    
    return jsonify({
        'success': result.get('success', False),
        'agent_id': agent_id,
        'result': result,
        'state': builder.get_state()
    })


@builder_bp.route('/<agent_id>/task', methods=['POST'])
def set_builder_task(agent_id: str):
    """
    Set builder's current task
    
    POST /api/builder/{agent_id}/task
    Body: { "task": "Gather 100 wood" }
    """
    from app import grid_manager
    
    builder = get_or_create_builder(agent_id, grid_manager)
    
    data = request.json or {}
    task = data.get('task')
    
    builder.current_task = task
    
    return jsonify({
        'success': True,
        'agent_id': agent_id,
        'task': task,
        'state': builder.get_state()
    })


@builder_bp.route('/<agent_id>/inventory', methods=['GET'])
def get_builder_inventory(agent_id: str):
    """
    Get builder's inventory
    
    GET /api/builder/{agent_id}/inventory
    """
    if agent_id not in builders:
        return jsonify({
            'success': False,
            'error': f'Builder {agent_id} not found'
        }), 404
    
    builder = builders[agent_id]
    
    return jsonify({
        'success': True,
        'agent_id': agent_id,
        'inventory': builder.inventory
    })


@builder_bp.route('/<agent_id>/give', methods=['POST'])
def give_builder_resources(agent_id: str):
    """
    Give resources to builder
    
    POST /api/builder/{agent_id}/give
    Body: { "wood": 50, "stone": 20 }
    """
    from app import grid_manager
    
    builder = get_or_create_builder(agent_id, grid_manager)
    
    data = request.json or {}
    
    if 'wood' in data:
        builder.inventory['wood'] += int(data['wood'])
    if 'stone' in data:
        builder.inventory['stone'] += int(data['stone'])
    if 'food' in data:
        builder.inventory['food'] += int(data['food'])
    
    return jsonify({
        'success': True,
        'agent_id': agent_id,
        'inventory': builder.inventory
    })


@builder_bp.route('/<agent_id>/history', methods=['GET'])
def get_builder_history(agent_id: str):
    """
    Get builder's action history
    
    GET /api/builder/{agent_id}/history?limit=10
    """
    if agent_id not in builders:
        return jsonify({
            'success': False,
            'error': f'Builder {agent_id} not found'
        }), 404
    
    builder = builders[agent_id]
    limit = int(request.args.get('limit', 20))
    
    return jsonify({
        'success': True,
        'agent_id': agent_id,
        'action_count': len(builder.action_history),
        'history': builder.action_history[-limit:] if builder.action_history else []
    })


@builder_bp.route('/<agent_id>/simulate', methods=['POST'])
def simulate_builder(agent_id: str):
    """
    Run builder for N actions with 5-second delay between each
    
    POST /api/builder/{agent_id}/simulate
    Body: { "steps": 10, "delay": 5 }
    """
    import time
    from app import grid_manager
    
    builder = get_or_create_builder(agent_id, grid_manager)
    
    data = request.json or {}
    steps = int(data.get('steps', 5))
    delay = int(data.get('delay', 5))  # Default 5 seconds
    steps = min(steps, 50)  # Max 50 steps
    
    results = []
    
    for i in range(steps):
        print(f"\n⏱️ Step {i+1}/{steps} - Executing action...")
        
        result = builder.think_and_act()
        results.append({
            'step': i + 1,
            'action': result.get('action', 'unknown'),
            'success': result.get('success', False),
            'details': result
        })
        
        # Stop if action failed critically
        if not result.get('success', False) and result.get('action') == 'unknown':
            break
        
        # Wait between actions (except after last one)
        if i < steps - 1:
            print(f"⏳ Waiting {delay} seconds before next action...")
            time.sleep(delay)
    
    return jsonify({
        'success': True,
        'agent_id': agent_id,
        'steps_executed': len(results),
        'results': results,
        'final_state': builder.get_state()
    })


@builder_bp.route('/<agent_id>/delete', methods=['DELETE'])
def delete_builder(agent_id: str):
    """
    Delete a builder agent
    
    DELETE /api/builder/{agent_id}/delete
    """
    if agent_id not in builders:
        return jsonify({
            'success': False,
            'error': f'Builder {agent_id} not found'
        }), 404
    
    del builders[agent_id]
    
    return jsonify({
        'success': True,
        'message': f'Builder {agent_id} deleted'
    })


@builder_bp.route('/reset', methods=['POST'])
def reset_all_builders():
    """
    Delete all builders
    
    POST /api/builder/reset
    """
    count = len(builders)
    builders.clear()
    
    return jsonify({
        'success': True,
        'message': f'Deleted {count} builders'
    })

