# 🤖 Airia AI API Endpoints Reference

This document lists all Airia AI pipeline endpoints used in the project.

## Configuration

All endpoints require the `AIRIA_API_KEY` environment variable:

```bash
# Add to backend/.env
AIRIA_API_KEY=your_airia_api_key_here
```

## Endpoints

### 1. 🌍 World Analysis API (Oracle Environment Analyzer)

**Purpose:** Analyzes the game world to determine optimal Oracle spawn location and identify strategic resource zones.

**Pipeline ID:** `a019d481-6470-4b89-af5e-82c827b04c86`

**Endpoint:**
```bash
curl --location "https://api.airia.ai/v2/PipelineExecution/a019d481-6470-4b89-af5e-82c827b04c86" \
  --header "X-API-KEY: $AIRIA_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "userInput": "SYSTEM_PROMPT + WORLD_DATA",
    "asyncOutput": false
  }'
```

**Used In:**
- `backend/oracle_environment_analyzer.py`

**Input:** Tree locations, terrain tiles, map dimensions

**Output:** Oracle spawn position, tree clusters, resource zones, density analysis

**Documentation:**
- `ORACLE_ENVIRONMENT_SYSTEM.md`
- `ORACLE_ENVIRONMENT_QUICKSTART.md`
- `ORACLE_ENVIRONMENT_IMPLEMENTATION.md`

---

### 2. 🔮 Oracle Strategic AI

**Purpose:** Provides high-level strategic directives for Builder agents based on village needs.

**Pipeline ID:** `31a5bde8-9c32-4038-9fa0-f347df23aa52`

**Endpoint:**
```bash
curl --location "https://api.airia.ai/v2/PipelineExecution/31a5bde8-9c32-4038-9fa0-f347df23aa52" \
  --header "X-API-KEY: $AIRIA_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "userInput": "BUILDER_CONTEXT + VILLAGE_STATE",
    "asyncOutput": false
  }'
```

**Used In:**
- `backend/builder_oracle_orchestrator.py`

**Input:** Builder state, village resources, current priorities

**Output:** Strategic directive (e.g., "Gather wood from northern forest", "Build house near village center")

**Orchestration Flow:**
1. Builder state → Oracle Strategic AI
2. Oracle returns directive
3. Directive → Builder Tactical AI
4. Builder executes action

---

### 3. 🏗️ Builder Tactical AI

**Purpose:** Converts strategic directives into specific executable actions.

**Pipeline ID:** `3828632d-7e5a-4a21-a99d-fbcb9a49b1eb`

**Endpoint:**
```bash
curl --location "https://api.airia.ai/v2/PipelineExecution/3828632d-7e5a-4a21-a99d-fbcb9a49b1eb" \
  --header "X-API-KEY: $AIRIA_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "userInput": "ORACLE_DIRECTIVE + BUILDER_CONTEXT",
    "asyncOutput": false
  }'
```

**Used In:**
- `backend/builder_agent.py`
- `backend/builder_oracle_orchestrator.py`

**Input:** Oracle directive + Builder state (position, inventory, nearby resources)

**Output:** Action command string (TALK, WALK, CUT, BUILD)

**Available Actions:**
- `TALK "message"` - Log message
- `WALK x,y` - Move to position
- `CUT x,y,tree_id` - Cut tree
- `BUILD type,x,y` - Build structure

**Test Script:**
- `backend/test_builder.py`

---

### 3. 🧙‍♂️ Village Oracle API (Optional)

**Purpose:** Task assignment and resource management for villagers.

**Pipeline ID:** *(If using OpenAI instead, configure `OPENAI_API_KEY`)*

**Used In:**
- `backend/oracle_agent.py`
- `backend/village_api.py`

**Documentation:**
- `ORACLE_SYSTEM.md`
- `ORACLE_QUICKSTART.md`

---

## Testing Endpoints

### Test World Analysis API

```bash
# Create a test grid
cd backend
source venv/bin/activate
python test_oracle_environment.py
```

### Test Builder AI API

```bash
# Test builder actions
cd backend
source venv/bin/activate
python test_builder.py
```

### Manual API Test

```bash
# Set your API key
export AIRIA_API_KEY="your_key_here"

# Test World API
curl --location "https://api.airia.ai/v2/PipelineExecution/a019d481-6470-4b89-af5e-82c827b04c86" \
  --header "X-API-KEY: $AIRIA_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "userInput": "Analyze this 20x20 grid with 100 trees",
    "asyncOutput": false
  }'

# Test Builder API
curl --location "https://api.airia.ai/v2/PipelineExecution/3828632d-7e5a-4a21-a99d-fbcb9a49b1eb" \
  --header "X-API-KEY: $AIRIA_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "userInput": "Builder at position (5, 5) with 0 wood. There is a tree at (5, 6). What should I do?",
    "asyncOutput": false
  }'
```

---

## Fallback Behavior

All AI-powered systems have fallback logic if the API is unavailable or `AIRIA_API_KEY` is not configured:

### World Analysis Fallback
- Uses heuristic clustering algorithm
- Finds center position without trees
- Groups trees within 3-tile radius
- Instant analysis (<0.1s)

### Builder AI Fallback
- Uses rule-based decision tree
- Prioritizes wood gathering if inventory low
- Moves toward resources
- Builds when resources available

---

## API Response Formats

### World Analysis Response

```json
{
  "oracle_spawn": {
    "x": 10,
    "y": 10
  },
  "environment_memory": {
    "tree_count": 369,
    "tree_density": 0.9225,
    "tree_clusters": [
      {
        "cluster_id": 0,
        "center": { "x": 5, "y": 8 },
        "size": 12
      }
    ],
    "recommended_resource_zones": [
      { "x": 5, "y": 8 }
    ],
    "map_summary": "Map 20x20 with 369 trees (92.2% density)..."
  }
}
```

### Builder AI Response

```text
WALK 5,10
```

or

```text
CUT 5,6,42
```

or

```text
TALK "I need more wood for building"
```

---

## Rate Limits & Performance

| Endpoint | Response Time | Rate Limit |
|----------|---------------|------------|
| World Analysis | 1-3 seconds | Per Airia plan |
| Builder AI | 1-3 seconds | Per Airia plan |

**Optimization Tips:**
- Use fallback mode for development (faster)
- Batch operations when possible
- Cache analysis results
- Trigger re-analysis only on significant changes

---

## Environment Variables Summary

```bash
# Required for AI-powered features (optional - has fallbacks)
AIRIA_API_KEY=your_airia_api_key_here

# Optional - for village Oracle system
OPENAI_API_KEY=your_openai_api_key_here

# Required for tile/tree image generation
FREEPIK_API_KEY=your_freepik_api_key_here
```

---

## Support

- **Airia AI Documentation:** https://airia.ai/docs
- **Get API Key:** https://airia.ai
- **Project Docs:** See `ORACLE_ENVIRONMENT_SYSTEM.md`, `test_builder.py`

---

**Last Updated:** November 16, 2025  
**Project:** Campfire Autonomous Village Simulation

