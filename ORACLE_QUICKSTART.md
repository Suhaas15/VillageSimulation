# 🚀 Oracle System - Quick Start Guide

## Install Dependencies

```bash
cd backend
pip install openai colorama
```

## Start the Backend

```bash
python app.py
```

You should see:
```
✅ Village Oracle System loaded
🔑 Freepik API Key configured: Yes/No
🔑 OpenAI API Key configured: Yes/No (using fallback logic)
```

---

## 🎮 Run Your First Simulation

### Option 1: Use the Test Script (Recommended)
```bash
cd backend
python test_oracle.py
```

This runs an interactive demo showing:
- Village state
- Oracle decisions
- 5-day simulation
- Interactive mode

### Option 2: Use API Directly

#### Simulate 10 Days:
```bash
curl -X POST http://localhost:5001/api/village/simulate \
  -H "Content-Type: application/json" \
  -d '{"days": 10}'
```

#### Run One Oracle Cycle:
```bash
curl -X POST http://localhost:5001/api/village/cycle
```

---

## 📊 Check Village State

```bash
curl http://localhost:5001/api/village/state
```

**Example Response:**
```json
{
  "resources": {"wood": 150, "food": 120, "stone": 80},
  "villagers": [
    {"name": "Alice", "job": "lumberjack", "job_tier": 2, "stamina": 0.7, "experience": 75}
  ],
  "buildings": {"houses": 2, "workshops": 1, "farms": 1},
  "day": 15
}
```

---

## 🧙‍♂️ How the Oracle Works

### 1. You Call the Oracle
```bash
curl -X POST http://localhost:5001/api/village/oracle/consult
```

### 2. Oracle Analyzes State
- Checks resource levels
- Evaluates villager experience
- Determines priorities

### 3. Oracle Returns Decisions
```json
{
  "assignments": [
    {"name": "Alice", "new_job": "lumberjack", "job_tier": 2, "task": "chop_wood"},
    {"name": "Bob", "new_job": "farmer", "job_tier": 2, "task": "farm_crops"}
  ],
  "build_actions": [
    {"building": "house", "assigned_to": "Charlie"}
  ]
}
```

### 4. Apply Decisions & Execute
```bash
curl -X POST http://localhost:5001/api/village/oracle/apply -d '{...decisions...}'
curl -X POST http://localhost:5001/api/village/day/execute
```

Or use the combined endpoint:
```bash
curl -X POST http://localhost:5001/api/village/cycle
```

---

## 🎯 Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/village/state` | GET | Get current state |
| `/api/village/oracle/consult` | POST | Ask Oracle for decisions |
| `/api/village/cycle` | POST | Run complete cycle (consult + execute) |
| `/api/village/simulate` | POST | Simulate N days |
| `/api/village/reset` | POST | Reset to initial state |

---

## 📈 Watch Your Village Grow

### Initial State (Day 1):
- 3 Villagers (all tier 1)
- Resources: 50 wood, 50 food, 20 stone
- 1 House

### After 10 Days (typical):
- 3-4 Villagers (some promoted to tier 2)
- Resources: 200+ wood, 150+ food, 100+ stone
- 2-3 Houses, 1 Workshop

### After 30 Days (successful):
- 4-5 Villagers (tier 2-3)
- Resources: 500+ wood, 300+ food, 200+ stone
- 4-5 Houses, 2 Workshops, 1-2 Farms

---

## 🔧 Configuration

### Use AI Oracle (OpenAI)
```bash
echo "OPENAI_API_KEY=your_key_here" >> backend/.env
```

Restart backend to use GPT-4 for decisions.

### Use Fallback Logic (No API Key Needed)
The system works perfectly with built-in rule-based logic if no API key is provided.

---

## 🤖 Create Custom Agents

### Example: Resource Monitor Agent
```python
import requests
import time

def monitor_resources():
    while True:
        state = requests.get('http://localhost:5001/api/village/state').json()['state']
        
        if state['resources']['wood'] < 50:
            print("⚠️ ALERT: Low wood!")
            # Could trigger emergency response
        
        time.sleep(5)  # Check every 5 seconds

monitor_resources()
```

### Example: Auto-Builder Agent
```python
def auto_builder():
    state = requests.get('http://localhost:5001/api/village/state').json()['state']
    
    if state['resources']['wood'] >= 200:
        requests.post('http://localhost:5001/api/village/oracle/cycle')
        print("🏗️ Triggered building cycle")
```

---

## 🎮 Game Goals

### Beginner Goals:
- ✅ Reach 100 in each resource
- ✅ Build 3 houses
- ✅ Promote one villager to tier 2

### Intermediate Goals:
- ✅ Reach 500 wood, 300 food, 200 stone
- ✅ Build 5 houses, 2 workshops
- ✅ Have all tier 2 villagers

### Advanced Goals:
- ✅ Get a tier 3 villager (Builder/Chef/Engineer)
- ✅ Build 10 structures total
- ✅ Maintain 1000+ in all resources

---

## 📝 Example Output

```
==============================================================
DAY 5
==============================================================

🔮 Oracle assigned tasks:
   • Alice → chop_wood
   • Bob → farm_crops  
   • Charlie → mine_stone

⚡ Villagers worked:
   ✅ Alice +18 wood (stamina: 70%, exp: 42)
   ✅ Bob +16 food (stamina: 75%, exp: 38)
   ✅ Charlie +14 stone (stamina: 65%, exp: 35)

📊 RESOURCES: Wood=142, Food=116, Stone=74
🏘️ BUILDINGS: Houses=1, Workshops=0, Farms=0
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
cd backend
pip install flask flask-cors python-dotenv openai colorama
python app.py
```

### Oracle returns errors
- Check if OpenAI key is valid (if using AI mode)
- Oracle will automatically use fallback logic if AI fails
- Check logs for specific error messages

### Village not progressing
- Check if villagers have stamina (they need to rest)
- Verify Oracle is assigning appropriate tasks
- Check resource levels - might be stuck waiting for a specific resource

---

## 🎉 You're Ready!

Run this to see it in action:
```bash
cd backend
python test_oracle.py
```

Or start building your own agents using the API!

See `ORACLE_SYSTEM.md` for complete documentation.

**Happy village building!** 🏘️✨

