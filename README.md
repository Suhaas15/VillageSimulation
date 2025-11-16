# 🌳 The Village Simulation

> An autonomous AI-driven village simulation with dynamic grid-based world generation, resource management, intelligent Oracle and Builder agents, and evolving gameplay.

<div align="center">

![Grid System](https://img.shields.io/badge/Grid-40x40-green)
![AI Agents](https://img.shields.io/badge/AI%20Agents-Oracle%20%26%20Builder-blue)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![React](https://img.shields.io/badge/React-18-61DAFB)
![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey)

</div>

---

## ✨ Features

### 🗺️ World System
- **40x40 Dynamic Grid** with viewport-based rendering for optimal performance
- **Multiple Tile Types**: Grass, Dirt, Forest, and Water biomes
- **Random Tree Generation** (1,000+ trees with 3 species: Oak, Pine, Birch)
- **Interactive Resource Gathering** - click trees to harvest wood
- **Pan & Zoom Navigation** for exploring the expansive world
- **AI-Generated Tiles** via Freepik API integration

### 🤖 AI Agent System
- **Oracle Agent**: Governing AI that analyzes environment and makes strategic decisions
- **Builder Agent**: Autonomous villager that gathers resources and builds structures
- **Oracle-Builder Orchestration**: Coordinated AI workflow where Oracle guides Builder actions
- **Environment Analysis**: Oracle evaluates world state and provides contextual guidance
- **Personality-Driven Behavior**: Each agent has unique characteristics and decision-making patterns

### 📊 Resource Management
- **Wood**: Harvested from trees (5-15 units per tree)
- **Stone**: Mining resources (planned)
- **Food**: Gathering system (planned)
- **Real-time tracking** with visual resource panel

### 🎮 Gameplay
- **Interactive World**: Click and drag to pan, click resources to gather
- **Agent Spawning**: Spawn Oracle and Builder agents that interact autonomously
- **Activity Logging**: Real-time feed of all agent actions and decisions
- **Dynamic State Management**: Persistent village state across sessions

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+**
- **Node.js 16+**
- **npm** or **yarn**

### Installation

#### Option 1: One-Command Start (Recommended)
```bash
# Clone the repository
git clone https://github.com/Suhaas15/VillageSimulation.git
cd VillageSimulation

# Run the launcher
./start.sh
```

Open [http://localhost:3000](http://localhost:3000) in your browser! 🎉

#### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 📖 Usage

### Basic Controls

| Action | How To |
|--------|--------|
| **Pan camera** | Click and drag anywhere on the grid |
| **Cut tree** | Click on any tree to harvest wood |
| **Spawn Oracle** | Click "Spawn Oracle" button |
| **Spawn Builder** | Click "Spawn Builder" button |
| **Reset view** | Click "Reset View" button |
| **Refresh grid** | Click "Refresh Grid" button |

### AI Agent Workflow

1. **Spawn Oracle**: Creates the governing AI that analyzes the environment
2. **Oracle Analysis**: Oracle evaluates resources, terrain, and strategic opportunities
3. **Spawn Builder**: Creates a worker agent to execute tasks
4. **Builder Actions**: Builder autonomously gathers resources and builds based on Oracle guidance
5. **Watch Activity Log**: Real-time feed shows all agent decisions and actions

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     🌐 Browser (React)                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  VillageGrid  │  ResourcePanel  │  ActivityLog       │  │
│  │     Tile      │      Oracle     │     Builder        │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP/REST API
┌─────────────────────▼───────────────────────────────────────┐
│                 🐍 Flask Backend (Python)                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  app.py  │  grid_manager.py  │  village_state.py   │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  oracle_agent.py  │  builder_agent.py               │   │
│  │  oracle_environment_analyzer.py                      │   │
│  │  builder_oracle_orchestrator.py                      │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

- **`app.py`**: Flask API server with CORS-enabled endpoints
- **`grid_manager.py`**: 40x40 grid state management and tree generation
- **`village_state.py`**: Persistent village state and resource tracking
- **`oracle_agent.py`**: Oracle AI agent implementation
- **`builder_agent.py`**: Builder AI agent with autonomous behaviors
- **`oracle_environment_analyzer.py`**: Environment analysis for Oracle decision-making
- **`builder_oracle_orchestrator.py`**: Coordination layer between Oracle and Builder
- **`village_actions.py`**: Action system for agent behaviors
- **`freepik_api.py`**: AI tile generation integration

---

## 🔌 API Endpoints

### Grid & World

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/grid` | GET | Get complete grid state (1,600 tiles) |
| `/api/grid/viewport` | GET | Get viewport slice for optimization |
| `/api/grid/initialize` | POST | Initialize grid with AI-generated tiles |
| `/api/grid/reset` | POST | Reset grid to initial state |

### Resources

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/resources` | GET | Get current resource counts |
| `/api/tree/cut` | POST | Cut down a tree and gain wood |

### AI Agents

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/oracle/spawn` | POST | Spawn Oracle agent |
| `/api/oracle/analyze` | POST | Trigger Oracle environment analysis |
| `/api/builder/spawn` | POST | Spawn Builder agent |
| `/api/builder/act` | POST | Execute Builder action |
| `/api/village/state` | GET | Get complete village state |

---

## 🎨 Customization

### Change Grid Size
```python
# backend/grid_manager.py
def __init__(self, grid_size: int = 40):  # Change to 50, 60, etc.
```

### Change Tile Size
```javascript
// frontend/src/components/VillageGrid.jsx
const TILE_SIZE = 64 // Change to 32, 48, 128, etc.
```

### Change Tree Density
```python
# backend/grid_manager.py - in _generate_trees_for_tile()
num_trees = random.randint(1, 3)  # More trees per tile
```

### Add Custom Tile Images

1. Get a Freepik API key from [Freepik Developer Portal](https://www.freepik.com/api)
2. Create `.env` file in `backend/` directory:
```bash
FREEPIK_API_KEY=your_api_key_here
```
3. Call the initialization endpoint:
```bash
curl -X POST http://localhost:5001/api/grid/initialize
```

---

## 📁 Project Structure

```
VillageSimulation/
├── backend/                          # Python Flask API
│   ├── app.py                       # Main Flask server
│   ├── grid_manager.py              # Grid state management
│   ├── village_state.py             # Village persistence
│   ├── oracle_agent.py              # Oracle AI agent
│   ├── builder_agent.py             # Builder AI agent
│   ├── oracle_environment_analyzer.py  # Environment analysis
│   ├── builder_oracle_orchestrator.py  # Agent orchestration
│   ├── village_actions.py           # Action system
│   ├── freepik_api.py               # AI tile generation
│   └── requirements.txt             # Python dependencies
│
├── frontend/                         # React Frontend
│   ├── src/
│   │   ├── App.jsx                  # Main app component
│   │   └── components/
│   │       ├── VillageGrid.jsx      # Grid renderer with viewport optimization
│   │       ├── Tile.jsx             # Individual tile component
│   │       ├── Tree.jsx             # Tree overlay with click handling
│   │       ├── ResourcePanel.jsx    # Resource counter UI
│   │       ├── ActivityLog.jsx      # Agent activity feed
│   │       ├── Oracle.jsx           # Oracle agent UI
│   │       └── Builder.jsx          # Builder agent UI
│   ├── package.json
│   └── vite.config.js
│
├── start.sh                         # One-command launcher
├── README.md                        # This file
└── ARCHITECTURE.md                  # Detailed architecture docs
```

---

## 🤖 AI Agent System

### Oracle Agent
The Oracle is the governing intelligence of the village:
- **Environment Analysis**: Evaluates terrain, resources, and opportunities
- **Strategic Planning**: Determines optimal village development
- **Builder Guidance**: Provides instructions to Builder agents
- **Decision Making**: Uses AI-powered analysis for contextual decisions

### Builder Agent
The Builder is an autonomous worker:
- **Resource Gathering**: Automatically finds and harvests resources
- **Construction**: Builds structures based on Oracle guidance
- **Autonomous Behavior**: Makes independent decisions within Oracle's framework
- **Activity Logging**: Reports all actions to activity feed

### Orchestration
- Oracle analyzes environment and creates strategic plan
- Builder receives guidance and executes tasks
- Real-time coordination and feedback loop
- Activity log tracks all interactions

---

## 🛠️ Tech Stack

**Backend:**
- Python 3.9+
- Flask 3.0 (REST API)
- Flask-CORS (Cross-origin support)
- Requests (HTTP client for external APIs)
- Python-dotenv (Environment management)

**Frontend:**
- React 18 (UI framework)
- Vite 5 (Build tool & dev server)
- Axios (HTTP client)
- CSS3 (Styling with no frameworks)

**APIs:**
- Freepik API (AI tile generation)
- AIRIA API (Agent workflows - optional)

---

## 🐛 Troubleshooting

### Port Issues

**Port 5001 already in use:**
```bash
lsof -ti:5001 | xargs kill -9
```
> Note: Port 5000 is used by macOS AirPlay, so we use 5001 instead.

**Port 3000 already in use:**
```bash
lsof -ti:3000 | xargs kill -9
```

### Module Not Found

**Python:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Node:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Trees Not Appearing
- Check browser console for errors
- Ensure backend is running on port 5001
- Try refreshing the grid with the "Refresh Grid" button

### Grid Not Loading
- Verify Flask server is running: `curl http://localhost:5001/api/health`
- Check CORS is enabled in `app.py`
- Open browser developer tools and check Network tab

### Performance Issues
- The viewport system only renders visible tiles (~100-200 instead of 1,600)
- If still slow, reduce grid size in `grid_manager.py`
- Close other resource-intensive applications

---

## 🗺️ Roadmap

### ✅ Phase 1: World Foundation (COMPLETE)
- [x] 40x40 grid system
- [x] Tile types and generation
- [x] Tree placement and harvesting
- [x] Resource tracking
- [x] Pan/zoom navigation
- [x] Viewport optimization

### ✅ Phase 2: AI Agents (COMPLETE)
- [x] Oracle agent implementation
- [x] Builder agent implementation
- [x] Environment analyzer
- [x] Oracle-Builder orchestration
- [x] Activity logging system
- [x] Agent spawning UI

### 🚧 Phase 3: Advanced Simulation (IN PROGRESS)
- [ ] Building construction system
- [ ] Multiple Builder agents
- [ ] Agent pathfinding
- [ ] Day/night cycle
- [ ] Weather system

### 🔮 Phase 4: Evolution & Complexity (PLANNED)
- [ ] Agent personality evolution
- [ ] Villager relationships
- [ ] Trade system
- [ ] Technology tree
- [ ] Multi-village interactions

---

## 📝 License

MIT License - Feel free to build awesome stuff with this!

---

## 🎉 Contributing

Contributions are welcome! This project is perfect for:
- AI/ML enthusiasts interested in agent-based systems
- Game developers exploring procedural generation
- Full-stack developers wanting to work with React + Flask
- Anyone interested in autonomous simulation systems

**To contribute:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🌟 Acknowledgments

Built with ❤️ for autonomous AI simulations and emergent gameplay.

**Technologies & APIs:**
- [React](https://react.dev/) - Frontend framework
- [Flask](https://flask.palletsprojects.com/) - Backend API
- [Vite](https://vitejs.dev/) - Build tool
- [Freepik API](https://www.freepik.com/api) - AI image generation

---

<div align="center">

**[Documentation](./ARCHITECTURE.md)** • **[Quick Start](./QUICKSTART.md)** • **[Troubleshooting](./TROUBLESHOOTING.md)**

Made with 🌳 by the Village Simulation Team

</div>
