# 🚀 Oracle Environment Analyzer - Quick Start Guide

## What is it?

The Oracle Environment Analyzer is an AI-powered system that:
- 🔍 Analyzes the game world (trees, terrain, layout)
- 🎯 Chooses optimal Oracle spawn location
- 🗺️ Identifies resource-rich zones
- 🌲 Tracks tree clusters
- 🔄 Updates automatically when environment changes

## Setup (1 minute)

### 1. Get Airia AI API Key

```bash
# Sign up at https://airia.ai
# Copy your API key
```

### 2. Configure Environment

```bash
cd backend
echo "AIRIA_API_KEY=your_api_key_here" >> .env
```

### 3. Verify Installation

```bash
cd backend
python test_oracle_environment.py
```

✅ You should see environment analysis output!

## How It Works

### Automatic Triggers

1️⃣ **Grid Initialization**
```python
grid = GridManager(grid_size=40)
# → Oracle AI analyzes world automatically
# → Oracle spawns at optimal location
```

2️⃣ **Tree Cutting**
```python
grid.cut_tree(x, y, tree_id)
# → Oracle AI re-analyzes environment
# → Oracle may reposition if needed
```

### What You Get

```json
{
  "oracle_spawn": {
    "x": 20,
    "y": 20
  },
  "environment_memory": {
    "tree_count": 450,
    "tree_density": 0.28,
    "tree_clusters": [
      {
        "cluster_id": 0,
        "center": { "x": 15, "y": 25 },
        "size": 12
      }
    ],
    "recommended_resource_zones": [
      { "x": 15, "y": 25 }
    ],
    "map_summary": "Map 40x40 with 450 trees..."
  }
}
```

## Using the API

### Start Backend

```bash
cd backend
source venv/bin/activate
python app.py
```

### Get Current Analysis

```bash
curl http://localhost:5001/api/oracle/environment
```

**Response:**
```json
{
  "success": true,
  "analysis": { /* analysis data */ }
}
```

### Trigger Re-Analysis

```bash
curl -X POST http://localhost:5001/api/oracle/analyze
```

### Get Full Grid State (includes analysis)

```bash
curl http://localhost:5001/api/grid
```

## Python Usage

```python
from grid_manager import GridManager

# Create grid (auto-analyzes)
grid = GridManager(grid_size=40)

# Access analysis
analysis = grid.environment_analysis

if analysis:
    # Get Oracle spawn location
    spawn = analysis['oracle_spawn']
    print(f"Oracle at: ({spawn['x']}, {spawn['y']})")
    
    # Get environment insights
    memory = analysis['environment_memory']
    print(f"Trees: {memory['tree_count']}")
    print(f"Density: {memory['tree_density']:.2%}")
    print(f"Clusters: {len(memory['tree_clusters'])}")
    
    # Get resource zones
    zones = memory['recommended_resource_zones']
    print(f"Resource zones: {zones}")

# Cut tree (auto re-analyzes)
success, wood = grid.cut_tree(10, 15, 5)

# Check updated analysis
new_memory = grid.environment_analysis['environment_memory']
print(f"Trees remaining: {new_memory['tree_count']}")
```

## Testing

### Run Test Script

```bash
cd backend
python test_oracle_environment.py
```

**What it does:**
1. ✅ Creates 40x40 grid
2. 🔮 Triggers Oracle AI analysis
3. 📍 Shows Oracle spawn location
4. 🌲 Displays tree clusters
5. 🪓 Cuts 5 trees
6. 🔄 Shows re-analysis after each cut
7. 💾 Exports analysis to `oracle_analysis.json`

**Expected Output:**
```
🔮 ORACLE ENVIRONMENT ANALYZER TEST
====================================================================

✅ AIRIA_API_KEY configured: sk-...

1️⃣ INITIALIZING GRID
====================================================================
✅ Grid initialized with 450 trees

🔮 Calling Oracle AI for environment analysis...
✅ Oracle AI analysis complete
🧙‍♂️ Oracle spawn updated to: (20, 20)

2️⃣ INITIAL ENVIRONMENT ANALYSIS
====================================================================
📍 Oracle Spawn Location:
   Position: (20, 20)

🌍 Environment Memory:
   🌲 Total Trees: 450
   📊 Tree Density: 28.12%
   🗺️ Tree Clusters: 5
   ...
```

## No API Key? No Problem!

If `AIRIA_API_KEY` is not set, the system automatically uses **fallback heuristic analysis**:

✅ Still analyzes environment  
✅ Still chooses optimal spawn  
✅ Still detects clusters  
❌ Less intelligent (rule-based instead of AI)  

**Fallback is instant** (<0.1s) vs AI (~1-3s)

## Integration with Village Oracle

The Environment Analyzer works with the Village Oracle system:

```
Environment Analyzer          Village Oracle
       ↓                            ↓
 Identifies resource zones → Assigns woodcutters
       ↓                            ↓
 Trees are cut            → Re-analyzes world
       ↓                            ↓
 New zones discovered     → Reassigns villagers
```

## Common Use Cases

### 1. Display Oracle on Map

```javascript
// Frontend
const analysis = await axios.get('/api/oracle/environment')
const { x, y } = analysis.data.analysis.oracle_spawn

// Render Oracle sprite at (x, y)
renderOracle(x, y)
```

### 2. Highlight Resource Zones

```javascript
const zones = analysis.data.analysis.environment_memory.recommended_resource_zones

zones.forEach(zone => {
  highlightTile(zone.x, zone.y, 'resource-rich')
})
```

### 3. Track Tree Density

```python
# Monitor deforestation
analysis = grid.environment_analysis
density = analysis['environment_memory']['tree_density']

if density < 0.15:
    print("⚠️ Warning: Low tree density, need reforestation!")
```

### 4. Guide Villagers to Clusters

```python
# Send woodcutters to biggest cluster
clusters = analysis['environment_memory']['tree_clusters']
biggest_cluster = max(clusters, key=lambda c: c['size'])

print(f"Send woodcutter to: ({biggest_cluster['center']['x']}, {biggest_cluster['center']['y']})")
```

## Troubleshooting

### ❌ "Oracle analysis failed"

**Check:**
```bash
# Is AIRIA_API_KEY set?
echo $AIRIA_API_KEY

# Is it in .env file?
cat backend/.env | grep AIRIA_API_KEY

# Test API directly
curl -X POST https://api.airia.ai/v2/PipelineExecution/... \
  -H "X-API-KEY: $AIRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"userInput": "test", "asyncOutput": false}'
```

**Solution:**
System will use fallback heuristics automatically. No action needed.

### ❌ Analysis is slow

**Causes:**
- Network latency to Airia AI API
- Large grid size (more data to process)

**Solutions:**
```python
# Option 1: Use fallback mode (instant)
# Don't set AIRIA_API_KEY

# Option 2: Batch re-analysis (modify grid_manager.py)
self.trees_cut_since_analysis += 1
if self.trees_cut_since_analysis >= 10:  # Re-analyze every 10 trees
    self._analyze_environment()
    self.trees_cut_since_analysis = 0
```

### ❌ Oracle spawns in wrong location

**Debug:**
```python
# Check analysis details
analysis = grid.environment_analysis
print(json.dumps(analysis, indent=2))

# Check if Oracle position was updated
print(f"Oracle at: {grid.oracle_position}")

# Check if position is valid (no trees)
tile_key = f"{grid.oracle_position['x']},{grid.oracle_position['y']}"
tile = grid.grid[tile_key]
active_trees = [t for t in tile['trees'] if not t['cut']]
print(f"Trees at Oracle location: {len(active_trees)}")  # Should be 0
```

## Performance Tips

### Reduce API Calls

```python
# Don't re-analyze on every tree cut
# Instead, batch them:

class GridManager:
    def __init__(self):
        self.trees_cut_since_analysis = 0
    
    def cut_tree(self, x, y, tree_id):
        # ... cut tree logic ...
        
        self.trees_cut_since_analysis += 1
        
        # Only re-analyze every 10 trees
        if self.trees_cut_since_analysis >= 10:
            self._analyze_environment()
            self.trees_cut_since_analysis = 0
```

### Cache Results

```python
# Don't fetch analysis repeatedly
analysis = grid.environment_analysis  # Cached in memory

# Only fetch if you need latest
grid._analyze_environment()  # Trigger new analysis
analysis = grid.environment_analysis  # Get fresh results
```

## API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/oracle/environment` | Get current analysis |
| POST | `/api/oracle/analyze` | Trigger re-analysis |
| GET | `/api/grid` | Get grid state (includes analysis) |
| POST | `/api/tree/cut` | Cut tree (triggers re-analysis) |

## Next Steps

1. ✅ **Read full documentation**: `ORACLE_ENVIRONMENT_SYSTEM.md`
2. ✅ **Integrate with frontend**: Display Oracle and resource zones on map
3. ✅ **Connect to Village Oracle**: Use resource zones for villager assignments
4. ✅ **Customize prompts**: Modify `ORACLE_SYSTEM_PROMPT` for different strategies
5. ✅ **Add visualizations**: Heat maps, cluster overlays, density gradients

## Support

- 📖 Full Documentation: `ORACLE_ENVIRONMENT_SYSTEM.md`
- 🧪 Test Script: `backend/test_oracle_environment.py`
- 🏗️ Implementation: `backend/oracle_environment_analyzer.py`
- 🌐 API: `backend/app.py` (endpoints)

Happy building! 🎮🌲🔮

