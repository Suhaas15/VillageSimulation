# 🧙‍♂️ VILLAGE ORACLE SYSTEM - Complete Documentation

## Overview

An autonomous village simulation where an AI Oracle makes all decisions for resource management, villager assignments, and building construction. The Oracle analyzes the village state and issues commands that agents execute.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     VILLAGE SIMULATION                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────┐ │
│  │   VILLAGE    │─────▶│   ORACLE AI  │◀─────│  AGENTS  │ │
│  │    STATE     │      │   (Decision  │      │          │ │
│  │              │      │    Maker)    │      │          │ │
│  └──────────────┘      └──────────────┘      └──────────┘ │
│         │                      │                      │    │
│         │                      │                      │    │
│         ▼                      ▼                      ▼    │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────┐ │
│  │   ACTIONS    │      │  PROMOTIONS  │      │   TASKS  │ │
│  │   HANDLER    │      │   & JOBS     │      │   QUEUE  │ │
│  └──────────────┘      └──────────────┘      └──────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Components

### 1. Village State (`village_state.py`)
Manages the complete village simulation state:
- **Resources**: Wood, Food, Stone
- **Villagers**: Name, Job, Tier, Stamina, Experience, Assigned Task
- **Buildings**: Houses, Workshops, Farms
- **Day Counter**: Current simulation day

### 2. Actions Handler (`village_actions.py`)
Defines all actions villagers can perform:

#### Resource Gathering Actions:
- `chop_wood` - Woodcutter/Lumberjack/Builder
- `gather_food` - Forager
- `farm_crops` - Farmer/Chef
- `cook_food` - Chef (consumes raw food, produces more)
- `mine_stone` - Miner/Excavator/Engineer

#### Building Actions:
- `build_house` - Costs: 50 wood, 30 stone
- `build_workshop` - Costs: 80 wood, 60 stone
- `build_farm` - Costs: 40 wood, 20 food

#### Recovery Action:
- `rest` - Restores stamina

### 3. Oracle Agent (`oracle_agent.py`)
AI decision-maker using OpenAI GPT or fallback logic:
- Analyzes village state
- Makes promotion decisions
- Assigns tasks to villagers
- Prioritizes resource gathering
- Triggers building construction

### 4. Village API (`village_api.py`)
Flask REST API endpoints for the system

---

## 🔌 API Endpoints

### Get Village State
```bash
GET /api/village/state
```

**Response:**
```json
{
  "success": true,
  "state": {
    "resources": {
      "wood": 50,
      "food": 50,
      "stone": 20
    },
    "villagers": [
      {
        "name": "Alice",
        "job": "woodcutter",
        "job_tier": 1,
        "stamina": 1.0,
        "experience": 0,
        "assigned_task": null
      }
    ],
    "buildings": {
      "houses": 1,
      "workshops": 0,
      "farms": 0
    },
    "day": 1
  }
}
```

### Consult Oracle
```bash
POST /api/village/oracle/consult
```

**Response:**
```json
{
  "success": true,
  "decisions": {
    "assignments": [
      {
        "name": "Alice",
        "new_job": "woodcutter",
        "job_tier": 1,
        "task": "chop_wood"
      }
    ],
    "build_actions": []
  },
  "day": 1
}
```

### Apply Oracle Decisions
```bash
POST /api/village/oracle/apply

{
  "assignments": [...],
  "build_actions": [...]
}
```

### Execute One Day
```bash
POST /api/village/day/execute
```

All villagers perform their assigned tasks.

### Run Complete Oracle Cycle
```bash
POST /api/village/cycle
```

Combines: Consult Oracle → Apply Decisions → Execute Day

### Simulate Multiple Days
```bash
POST /api/village/simulate

{
  "days": 10
}
```

Runs autonomous simulation for N days.

### Reset Village
```bash
POST /api/village/reset
```

### Add Villager
```bash
POST /api/village/villager/add

{
  "name": "David",
  "job": "miner",
  "job_tier": 1
}
```

### Add Resources (Admin)
```bash
POST /api/village/resources/add

{
  "wood": 100,
  "food": 50,
  "stone": 30
}
```

---

## 🧱 Job System

### Job Trees (3 Tiers Each)

#### 🌲 Wood Path
1. **Woodcutter** (T1) → Gathers 10 wood/day
2. **Lumberjack** (T2) → Gathers 15 wood/day (50% more efficient)
3. **Builder** (T3) → Gathers 20 wood/day, can construct buildings

#### 🌾 Food Path
1. **Forager** (T1) → Gathers 8 food/day
2. **Farmer** (T2) → Farms 15 food/day (stable production)
3. **Chef** (T3) → Cooks 20 food/day (consumes 10 raw food)

#### ⛏ Stone Path
1. **Miner** (T1) → Mines 12 stone/day
2. **Excavator** (T2) → Mines 18 stone/day (fast mining)
3. **Engineer** (T3) → Mines 24 stone/day, assists builders

### Promotion Rules

**Woodcutter → Lumberjack:**
- Experience > 70

**Lumberjack → Builder:**
- Experience > 85
- Village has wood > 200

**Forager → Farmer:**
- Experience > 70

**Farmer → Chef:**
- Experience > 90
- Village has food > 200

**Miner → Excavator:**
- Experience > 70

**Excavator → Engineer:**
- Experience > 90
- Village has stone > 150

---

## 🧠 Oracle Decision Logic

### 1. Resource Priority System

```
If wood < 100:
  Priority: WOOD
  → All wood workers → chop_wood
  → Consider promoting to lumberjack

If food < 100:
  Priority: FOOD
  → Foragers → gather_food
  → Farmers → farm_crops
  → Consider promoting to farmer

If stone < 80:
  Priority: STONE
  → All miners → mine_stone
  → Consider promoting to excavator
```

### 2. Building Triggers

```
If wood ≥ 200:
  → Assign builder to build_house

If stone ≥ 150 AND wood ≥ 100:
  → Assign engineer to build_workshop

If food ≥ 180:
  → Assign farmer/chef to build_farm
```

### 3. Stamina Management

```
If villager.stamina < 0.2:
  → Assign "rest" (overrides all other tasks)
```

---

## 🎮 Usage Examples

### Example 1: Basic Autonomous Cycle

```bash
# Run one complete cycle
curl -X POST http://localhost:5001/api/village/cycle
```

### Example 2: Simulate 10 Days
```bash
curl -X POST http://localhost:5001/api/village/simulate \
  -H "Content-Type: application/json" \
  -d '{"days": 10}'
```

### Example 3: Manual Control
```bash
# 1. Get current state
curl http://localhost:5001/api/village/state

# 2. Consult Oracle
curl -X POST http://localhost:5001/api/village/oracle/consult

# 3. Apply decisions (manually or from Oracle)
curl -X POST http://localhost:5001/api/village/oracle/apply \
  -H "Content-Type: application/json" \
  -d '{
    "assignments": [
      {"name": "Alice", "new_job": "woodcutter", "job_tier": 1, "task": "chop_wood"}
    ],
    "build_actions": []
  }'

# 4. Execute the day
curl -X POST http://localhost:5001/api/village/day/execute
```

---

## 🤖 Agent Integration

### Creating Additional Agents

You can create specialized agents that interact with the Oracle:

#### Example: Resource Monitor Agent
```python
import requests

def resource_monitor_agent():
    """Agent that monitors resources and alerts"""
    response = requests.get('http://localhost:5001/api/village/state')
    state = response.json()['state']
    
    resources = state['resources']
    
    if resources['wood'] < 50:
        print("⚠️ ALERT: Wood critically low!")
        # Could trigger emergency wood gathering
    
    if resources['food'] < 50:
        print("⚠️ ALERT: Food critically low!")
        # Could request Oracle to prioritize food
```

#### Example: Building Planner Agent
```python
def building_planner_agent():
    """Agent that plans building construction"""
    response = requests.get('http://localhost:5001/api/village/state')
    state = response.json()['state']
    
    resources = state['resources']
    buildings = state['buildings']
    villagers = state['villagers']
    
    # Count tier 3 workers
    builders = [v for v in villagers if v['job'] in ['builder', 'engineer']]
    
    if len(builders) > 0 and resources['wood'] >= 200:
        print("💡 Suggestion: Build a house")
        # Could submit building request to Oracle
```

---

## 🔧 Configuration

### Environment Variables (`.env`)

```bash
# Optional: OpenAI API key for Oracle AI
OPENAI_API_KEY=your_openai_key_here

# If not provided, Oracle uses rule-based fallback logic
```

### Tuning Parameters

Edit `village_actions.py` to adjust:
- Resource yields
- Stamina costs
- Experience gains
- Building costs

Edit `oracle_agent.py` to adjust:
- Promotion thresholds
- Resource priority levels
- Building triggers

---

## 📊 Metrics & Analytics

### Track Progress
```python
import requests
import time

def track_simulation(days=30):
    """Track village progress over time"""
    history = []
    
    for day in range(days):
        # Run cycle
        requests.post('http://localhost:5001/api/village/cycle')
        
        # Get state
        response = requests.get('http://localhost:5001/api/village/state')
        state = response.json()['state']
        
        history.append({
            'day': state['day'],
            'wood': state['resources']['wood'],
            'food': state['resources']['food'],
            'stone': state['resources']['stone'],
            'houses': state['buildings']['houses'],
            'villagers': len(state['villagers'])
        })
        
        time.sleep(0.5)
    
    return history
```

---

## 🎯 Future Enhancements

### Planned Features:
1. **Multiple Agents**: Specialist agents for different aspects
2. **Agent Communication**: Agents can message each other
3. **Emergency Events**: Random events requiring quick decisions
4. **Research Tree**: Unlock new jobs and buildings
5. **Population Growth**: Villagers have children in houses
6. **Combat System**: Defend against threats
7. **Trading System**: Exchange resources with other villages

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
cd backend
pip install flask flask-cors python-dotenv openai
```

### 2. Set Up Environment
```bash
# Optional: Add OpenAI key for AI Oracle
echo "OPENAI_API_KEY=your_key" >> .env
```

### 3. Start Server
```bash
python app.py
```

### 4. Run First Simulation
```bash
curl -X POST http://localhost:5001/api/village/simulate -H "Content-Type: application/json" -d '{"days": 5}'
```

---

## 📝 Example Output

```
==============================================================
DAY 1
==============================================================

✅ Alice +12 wood (stamina: 85%, exp: 5)
✅ Bob +9 food (stamina: 88%, exp: 5)
✅ Charlie +14 stone (stamina: 80%, exp: 6)

📊 RESOURCES: Wood=62, Food=59, Stone=34
🏘️ BUILDINGS: Houses=1, Workshops=0, Farms=0

==============================================================
DAY 2
==============================================================

⬆️ Alice: woodcutter (T1) → lumberjack (T2)
✅ Alice +18 wood (stamina: 70%, exp: 78)
✅ Bob +10 food (stamina: 76%, exp: 78)
✅ Charlie +15 stone (stamina: 60%, exp: 74)

📊 RESOURCES: Wood=80, Food=69, Stone=49
🏘️ BUILDINGS: Houses=1, Workshops=0, Farms=0
```

---

**The Oracle System is ready! All agents can now consult the Oracle and execute its wisdom.** 🧙‍♂️✨

