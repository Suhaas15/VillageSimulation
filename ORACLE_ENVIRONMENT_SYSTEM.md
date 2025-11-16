# 🔮 Oracle Environment Analyzer System

## Overview

The **Oracle Environment Analyzer** is an intelligent system that uses AI to analyze the game world and make strategic decisions about Oracle placement and resource management. It automatically triggers on grid initialization and whenever the environment changes (e.g., trees are cut).

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Grid Initialization                       │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              Oracle Environment Analyzer                     │
│  1. Extract grid data (trees, terrain, dimensions)          │
│  2. Call Airia AI API with analysis prompt                  │
│  3. Parse AI response (spawn location + strategy)           │
│  4. Update grid manager with results                        │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  Store Analysis Results                      │
│  - oracle_spawn: { x, y }                                   │
│  - environment_memory: {                                     │
│      tree_count, tree_density, tree_clusters,               │
│      recommended_resource_zones, map_summary                │
│    }                                                         │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              Automatic Re-Analysis Triggers                  │
│  • When trees are cut (environment changed)                 │
│  • Manual trigger via API (/api/oracle/analyze)            │
└─────────────────────────────────────────────────────────────┘
```

## System Components

### 1. `oracle_environment_analyzer.py`

The core analyzer class that:
- Extracts grid data (tree locations, terrain tiles)
- Calls Airia AI API for strategic analysis
- Falls back to heuristic analysis if API unavailable
- Stores results for future reference

**Key Methods:**
- `extract_grid_data(grid_manager)` - Gather current world state
- `call_oracle_ai(grid_data)` - Invoke Airia AI for analysis
- `_fallback_analysis(grid_data)` - Heuristic backup if API fails
- `analyze_and_update(grid_manager)` - Full analysis pipeline

### 2. `grid_manager.py` Integration

The grid manager now:
- Initializes Oracle analyzer on creation
- Calls `_analyze_environment()` after grid setup
- Automatically re-analyzes when trees are cut
- Stores analysis results in `environment_analysis` attribute

**New Attributes:**
- `oracle_analyzer` - Instance of OracleEnvironmentAnalyzer
- `environment_analysis` - Latest AI analysis results

**Modified Methods:**
- `__init__()` - Creates analyzer instance
- `initialize_grid()` - Triggers initial analysis
- `cut_tree()` - Triggers re-analysis after each cut

### 3. API Endpoints (`app.py`)

Two new endpoints for accessing Oracle analysis:

#### GET `/api/oracle/environment`
Get the current environment analysis without triggering re-analysis.

**Response:**
```json
{
  "success": true,
  "analysis": {
    "oracle_spawn": { "x": 20, "y": 20 },
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
      "map_summary": "Map 40x40 with 450 trees (28% density)..."
    }
  }
}
```

#### POST `/api/oracle/analyze`
Manually trigger a new environment analysis.

**Response:**
```json
{
  "success": true,
  "message": "Environment analysis completed",
  "analysis": { /* same structure as above */ }
}
```

## Airia AI Integration

### API Configuration

The system uses the **Airia AI Pipeline API** for environment analysis.

**Required Environment Variable:**
```bash
AIRIA_API_KEY=your_airia_api_key_here
```

**API Endpoint:**
```
POST https://api.airia.ai/v2/PipelineExecution/a019d481-6470-4b89-af5e-82c827b04c86
```

**Request Format:**
```json
{
  "userInput": "SYSTEM_PROMPT + WORLD_DATA",
  "asyncOutput": false
}
```

**Headers:**
```
X-API-KEY: your_api_key
Content-Type: application/json
```

### System Prompt

The Oracle receives this prompt defining its mission:

```
You are The Oracle, the central intelligence of the autonomous AI Village simulation.

Your first responsibility is to understand the environment by analyzing the initial world layout.

You receive the following input:

{
"tree_locations": [ { "x": int, "y": int }, ... ],
"terrain_tiles": [ ... ],
"map_width": int,
"map_height": int
}

Your goals:

1. Analyze the spatial layout.
2. Identify possible safe spawn positions for yourself (avoid trees).
3. Select the best Oracle spawn location using these rules:
   - Must not collide with a tree.
   - Prefer central coordinates on the map.
   - Prefer an open tile with maximum walking accessibility.
   - If multiple candidates exist, choose the closest to exact center.

4. Create a compact summary of the environment:
   - total trees
   - density of trees
   - clusters of trees
   - terrain distribution
   - strategic areas

5. Produce a structured memory object to store permanently:
   - oracle_spawn_position
   - map_summary
   - tree_clusters
   - resource_density

6. Output valid JSON only.

Output schema:

{
"oracle_spawn": { "x": int, "y": int },
"environment_memory": {
"tree_count": int,
"tree_density": float,
"tree_clusters": [
{
"cluster_id": int,
"center": { "x": int, "y": int },
"size": int
}
],
"recommended_resource_zones": [
{ "x": int, "y": int }
],
"map_summary": "short natural language summary for memory storage"
}
}

Do NOT output anything other than JSON.
Do NOT roleplay.
Do NOT invent objects that are not in the input.
Your output will be stored in long-term memory, so keep it accurate and compact.
```

### Input Data Format

The analyzer sends this data to the AI:

```json
{
  "tree_locations": [
    { "x": 5, "y": 10, "tree_id": 1 },
    { "x": 5, "y": 10, "tree_id": 2 },
    { "x": 12, "y": 8, "tree_id": 3 }
  ],
  "terrain_tiles": [
    { "x": 0, "y": 0, "type": "grass" },
    { "x": 0, "y": 1, "type": "grass" },
    { "x": 0, "y": 2, "type": "dirt" }
  ],
  "map_width": 40,
  "map_height": 40
}
```

### Expected Output

The AI returns strategic analysis in this format:

```json
{
  "oracle_spawn": {
    "x": 20,
    "y": 20
  },
  "environment_memory": {
    "tree_count": 450,
    "tree_density": 0.28125,
    "tree_clusters": [
      {
        "cluster_id": 0,
        "center": { "x": 15, "y": 25 },
        "size": 12
      },
      {
        "cluster_id": 1,
        "center": { "x": 30, "y": 10 },
        "size": 8
      }
    ],
    "recommended_resource_zones": [
      { "x": 15, "y": 25 },
      { "x": 30, "y": 10 }
    ],
    "map_summary": "Map 40x40 with 450 trees (28% density). Terrain: 1200 grass, 200 dirt, 200 water tiles. 5 tree clusters identified."
  }
}
```

## Fallback Logic

If Airia AI API is unavailable or fails, the system uses **heuristic fallback analysis**:

### Fallback Algorithm

1. **Count terrain types** - Calculate distribution of grass/dirt/water
2. **Calculate tree density** - `tree_count / total_tiles`
3. **Find center spawn** - Search for closest grass tile to map center without trees
4. **Simple clustering** - Group trees within 3 tiles of each other
5. **Identify resource zones** - Clusters with 5+ trees

### Fallback Output

The fallback produces the same JSON structure but with simpler analysis:

```python
{
    'oracle_spawn': best_spawn,
    'environment_memory': {
        'tree_count': tree_count,
        'tree_density': round(tree_density, 4),
        'tree_clusters': clusters,
        'recommended_resource_zones': resource_zones[:5],
        'map_summary': f"Map {width}x{height} with {tree_count} trees..."
    }
}
```

## Automatic Re-Analysis Triggers

### 1. Grid Initialization
When `GridManager` is created, it automatically triggers analysis:

```python
grid_manager = GridManager(grid_size=40)
# → _analyze_environment() called automatically
```

### 2. Tree Cutting
Every time a tree is cut, re-analysis is triggered:

```python
success, wood = grid_manager.cut_tree(x, y, tree_id)
# → _analyze_environment() called automatically
```

This keeps the Oracle's strategic understanding up-to-date as the world changes.

### 3. Manual Trigger
You can manually trigger re-analysis via API:

```bash
curl -X POST http://localhost:5001/api/oracle/analyze
```

Or programmatically:

```python
grid_manager._analyze_environment()
```

## Testing

### Run the Test Script

```bash
cd backend
python test_oracle_environment.py
```

**Test Workflow:**
1. ✅ Initialize grid (triggers first analysis)
2. 🪓 Cut 5 trees (triggers 5 re-analyses)
3. 📊 Display analysis evolution
4. 💾 Export final analysis to JSON

**Expected Output:**
```
🔮 ORACLE ENVIRONMENT ANALYZER TEST
====================================================================

✅ AIRIA_API_KEY configured: sk-proj...

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
   📊 Tree Density: 28%
   🗺️ Tree Clusters: 5
      • Cluster 0: 12 trees at (15, 25)
      • Cluster 1: 8 trees at (30, 10)
   🎯 Recommended Resource Zones: 2
      1. (15, 25)
      2. (30, 10)

   📝 Map Summary:
      Map 40x40 with 450 trees (28% density)...

...
```

## Integration with Existing Systems

### Village Oracle System

The **Environment Analyzer** complements the **Village Oracle System**:

- **Environment Analyzer** = Strategic world understanding
- **Village Oracle** = Villager task assignment

They work together:

1. Environment Analyzer identifies resource zones
2. Village Oracle assigns villagers to those zones
3. As villagers cut trees, Environment Analyzer updates strategy
4. Village Oracle adapts assignments based on new analysis

### Example Workflow

```python
# 1. Grid initialized → Environment analyzed
grid_manager = GridManager(grid_size=40)

# 2. Get resource zones from analysis
analysis = grid_manager.environment_analysis
resource_zones = analysis['environment_memory']['recommended_resource_zones']

# 3. Village Oracle assigns woodcutters to resource zones
# (Integration with village_state.py and oracle_agent.py)

# 4. Trees are cut → Environment re-analyzed
grid_manager.cut_tree(x, y, tree_id)

# 5. New resource zones discovered → Oracle reassigns villagers
```

## Usage Examples

### Python API

```python
from grid_manager import GridManager

# Initialize (triggers automatic analysis)
grid = GridManager(grid_size=40)

# Get current analysis
if grid.environment_analysis:
    spawn = grid.environment_analysis['oracle_spawn']
    memory = grid.environment_analysis['environment_memory']
    
    print(f"Oracle at: ({spawn['x']}, {spawn['y']})")
    print(f"Trees: {memory['tree_count']}")
    print(f"Density: {memory['tree_density']:.2%}")
    print(f"Clusters: {len(memory['tree_clusters'])}")

# Cut a tree (triggers re-analysis)
success, wood = grid.cut_tree(10, 15, tree_id=5)

# Get updated analysis
new_memory = grid.environment_analysis['environment_memory']
print(f"Trees remaining: {new_memory['tree_count']}")
```

### REST API

```bash
# Get current analysis
curl http://localhost:5001/api/oracle/environment

# Trigger re-analysis
curl -X POST http://localhost:5001/api/oracle/analyze

# Get full grid state (includes analysis)
curl http://localhost:5001/api/grid
```

### Frontend Integration (Future)

```javascript
// Fetch environment analysis
const response = await axios.get('/api/oracle/environment')
const analysis = response.data.analysis

// Display Oracle spawn on map
const { x, y } = analysis.oracle_spawn
renderOracleMarker(x, y)

// Highlight resource zones
analysis.environment_memory.recommended_resource_zones.forEach(zone => {
  highlightTile(zone.x, zone.y, 'resource-zone')
})

// Show tree clusters
analysis.environment_memory.tree_clusters.forEach(cluster => {
  renderClusterOverlay(cluster.center, cluster.size)
})
```

## Configuration

### Environment Variables

```bash
# Required for AI-powered analysis
AIRIA_API_KEY=your_airia_api_key_here

# Optional (system works with fallback if not set)
```

### Customization

You can customize the analysis behavior by modifying:

1. **System Prompt** - `ORACLE_SYSTEM_PROMPT` in `oracle_environment_analyzer.py`
2. **Fallback Logic** - `_fallback_analysis()` method
3. **Re-analysis Triggers** - Add custom triggers in `grid_manager.py`

## Performance Considerations

- **Initial Analysis**: ~1-3 seconds (depends on API latency)
- **Re-analysis on Tree Cut**: ~1-3 seconds per cut
- **Fallback Analysis**: <0.1 seconds (instant)

To avoid slowdowns when cutting many trees, consider:
- Batching re-analysis (every N trees instead of every tree)
- Using async analysis (set `asyncOutput: true` in API call)
- Caching analysis results (re-analyze only on significant changes)

## Troubleshooting

### Issue: "Oracle analysis failed"

**Possible Causes:**
- AIRIA_API_KEY not set
- API endpoint unreachable
- Invalid API response format

**Solution:**
System automatically falls back to heuristic analysis. Check logs for specific error.

### Issue: Oracle spawns in bad location

**With AI:**
- Check that tree data is being extracted correctly
- Verify AI is receiving correct input format
- Review AI response in logs

**With Fallback:**
- Fallback prefers center + grass + no trees
- If all center tiles have trees, it chooses the closest available grass tile

### Issue: Re-analysis too slow

**Solutions:**
- Use fallback mode (disable API)
- Batch re-analysis (every 5 trees instead of every tree)
- Cache analysis results
- Use `asyncOutput: true` for non-blocking

## Future Enhancements

1. **Smarter Re-analysis Triggers**
   - Only re-analyze if tree density drops below threshold
   - Re-analyze only affected regions (local analysis)

2. **Multi-Oracle Support**
   - Analyze optimal positions for multiple Oracles
   - Distribute Oracles across resource zones

3. **Predictive Analysis**
   - Predict future resource availability
   - Suggest expansion areas

4. **Historical Tracking**
   - Store analysis history over time
   - Visualize environment evolution

5. **Frontend Visualization**
   - Display Oracle spawn on map
   - Highlight resource zones
   - Show tree cluster heatmaps

## Summary

The **Oracle Environment Analyzer** provides intelligent, AI-powered strategic analysis of the game world:

✅ **Automatic** - Triggers on grid init and tree cuts  
✅ **Intelligent** - Uses AI to find optimal spawn locations  
✅ **Strategic** - Identifies clusters and resource zones  
✅ **Resilient** - Falls back to heuristics if AI unavailable  
✅ **Integrated** - Works with existing grid and Oracle systems  
✅ **API-First** - Accessible via REST endpoints  

It's a key component of the autonomous village simulation, providing the strategic intelligence layer that guides resource management and Oracle placement decisions.

