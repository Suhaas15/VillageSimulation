# 🔮 Oracle Environment Analyzer - Quick Reference

## What It Does

Automatically analyzes your game world and:
- 📍 Chooses optimal Oracle spawn location
- 🌲 Detects tree clusters (95 found!)
- 🎯 Recommends resource zones for woodcutting
- 📊 Tracks tree density (currently 94.2%)
- 🔄 Updates when trees are cut

## Current Status

✅ **FULLY OPERATIONAL**

```
Oracle Spawn: (17, 20)
Total Trees: 1,508
Tree Density: 94.2%
Tree Clusters: 95
Resource Zones: 5
```

## Quick Start

### 1. Get Current Analysis

```bash
curl http://localhost:5001/api/oracle/environment
```

### 2. Trigger Re-Analysis

```bash
curl -X POST http://localhost:5001/api/oracle/analyze
```

### 3. Python Usage

```python
from grid_manager import GridManager

grid = GridManager(grid_size=40)
analysis = grid.environment_analysis

print(f"Oracle at: {analysis['oracle_spawn']}")
print(f"Trees: {analysis['environment_memory']['tree_count']}")
print(f"Resource zones: {analysis['environment_memory']['recommended_resource_zones']}")
```

## How It Works

```
┌─────────────────────┐
│  Grid Initializes   │  → Automatic analysis
└─────────────────────┘
           │
           ▼
┌─────────────────────┐
│   Oracle Analyzes   │  → Finds best spawn
│   - Tree locations  │  → Detects clusters
│   - Terrain types   │  → Recommends zones
└─────────────────────┘
           │
           ▼
┌─────────────────────┐
│  Oracle Spawns at   │  → (17, 20)
│  Optimal Location   │
└─────────────────────┘
           │
           ▼
┌─────────────────────┐
│   Tree is Cut       │  → Triggers re-analysis
└─────────────────────┘  → Updates strategy
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/oracle/environment` | GET | Get current analysis |
| `/api/oracle/analyze` | POST | Trigger re-analysis |
| `/api/grid` | GET | Get grid + analysis |

## Files

| File | Purpose |
|------|---------|
| `backend/oracle_environment_analyzer.py` | Core analyzer |
| `backend/grid_manager.py` | Grid integration |
| `backend/app.py` | API endpoints |
| `backend/test_oracle_environment.py` | Test script |
| `ORACLE_ENVIRONMENT_SYSTEM.md` | Full docs |
| `ORACLE_ENVIRONMENT_QUICKSTART.md` | Quick guide |

## Example Output

```json
{
  "oracle_spawn": { "x": 17, "y": 20 },
  "environment_memory": {
    "tree_count": 1508,
    "tree_density": 0.9425,
    "tree_clusters": [
      {
        "cluster_id": 0,
        "center": { "x": 1, "y": 1 },
        "size": 11
      }
    ],
    "recommended_resource_zones": [
      { "x": 1, "y": 1 }
    ],
    "map_summary": "Map 40x40 with 1508 trees (94.2% density)..."
  }
}
```

## Features

✅ **Automatic** - Triggers on grid init and tree cuts  
✅ **Smart** - Finds optimal spawn locations  
✅ **Strategic** - Identifies resource-rich zones  
✅ **Fast** - <0.1s with fallback heuristics  
✅ **Reliable** - Works without API key  
✅ **Upgradeable** - Add AIRIA_API_KEY for AI power  

## Next Steps

### For Frontend Integration

```javascript
// 1. Fetch analysis
const { data } = await axios.get('/api/oracle/environment')

// 2. Display Oracle on map
const { x, y } = data.analysis.oracle_spawn
renderOracle(x, y)

// 3. Highlight resource zones
data.analysis.environment_memory.recommended_resource_zones.forEach(zone => {
  highlightTile(zone.x, zone.y, 'gold')
})
```

### For AI Power (Optional)

```bash
# 1. Get Airia AI key from https://airia.ai
# 2. Add to backend/.env
echo "AIRIA_API_KEY=your_key_here" >> backend/.env

# 3. Restart backend
cd backend && source venv/bin/activate && python app.py
```

## Documentation

- 📖 **Full Docs**: `ORACLE_ENVIRONMENT_SYSTEM.md`
- 🚀 **Quick Start**: `ORACLE_ENVIRONMENT_QUICKSTART.md`
- ✅ **Implementation**: `ORACLE_ENVIRONMENT_IMPLEMENTATION.md`

## Testing

```bash
# Run test script
cd backend
python test_oracle_environment.py

# Test API
curl http://localhost:5001/api/oracle/environment | python3 -m json.tool
```

## Support

**Current Mode:** Fallback Heuristic (fast & reliable)  
**Optional Upgrade:** Airia AI (intelligent & adaptive)  
**Status:** ✅ Production Ready

---

Built: November 15, 2025  
Version: 1.0.0  
Status: ✅ Operational 🚀

