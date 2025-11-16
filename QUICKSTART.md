# ⚡ Quick Start - Get Running in 2 Minutes

## 🚀 Fastest Way to Launch

```bash
# From project root
./start.sh
```

Then open: **http://localhost:3000** 🎉

---

## 📋 What You'll See

1. **40×40 Grid** with colored tiles (grass, dirt, forest, water)
2. **Random trees** (🌳 🌲 🌴) scattered across tiles
3. **Resource panel** at top showing Wood, Stone, Food counters
4. **Interactive trees** - hover to see highlight, click to cut

---

## 🎮 How to Use

| Action | How To |
|--------|--------|
| **Pan camera** | Click and drag anywhere |
| **Cut tree** | Click on any tree |
| **Reset view** | Click "Reset View" button |
| **Refresh grid** | Click "Refresh Grid" button |

---

## 🌳 Adding Your Tree PNG

1. Place `tree.png` in:
   ```
   frontend/public/tree.png
   ```

2. It will replace emojis automatically ✅

---

## 🎨 Customization Quick Wins

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
num_trees = random.randint(1, 3)  # More trees!
```

### Change Resource Gain

```python
# backend/grid_manager.py - in cut_tree()
wood_gained = random.randint(10, 25)  # More wood per tree
```

---

## 🛠️ Manual Start (Alternative)

### Terminal 1 - Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Terminal 2 - Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## ✅ Success Indicators

You'll know it's working when you see:

**Backend Terminal:**
```
🌳 Initializing Village Grid...
✅ Grid initialized: 40x40
 * Running on http://0.0.0.0:5000
```

**Frontend Terminal:**
```
  VITE v5.0.8  ready in 543 ms

  ➜  Local:   http://localhost:3000/
```

**Browser:**
- Gradient purple background
- Grid of colored tiles
- Trees scattered around
- Resource panel at top

---

## 🐛 Quick Fixes

### "Port 5001 already in use"
```bash
lsof -ti:5001 | xargs kill -9
```

**Note:** Port 5000 is used by macOS AirPlay, so we use 5001 instead.

### "Port 3000 already in use"
```bash
lsof -ti:3000 | xargs kill -9
```

### "Module not found" (Python)
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### "Module not found" (Node)
```bash
cd frontend
rm -rf node_modules
npm install
```

---

## 📁 File Structure

```
📦 Campfire_hack_nov_25/
│
├── 🚀 start.sh              ← Run this!
├── 📖 README.md             ← Full docs
├── ⚙️  SETUP.md              ← Detailed setup
├── 🏗️  ARCHITECTURE.md       ← System design
├── ⚡ QUICKSTART.md          ← This file
│
├── 🐍 backend/              ← Python Flask API
│   ├── app.py
│   ├── grid_manager.py
│   ├── freepik_api.py
│   └── requirements.txt
│
└── ⚛️  frontend/             ← React UI
    ├── src/
    │   ├── App.jsx
    │   └── components/
    │       ├── VillageGrid.jsx
    │       ├── Tile.jsx
    │       ├── Tree.jsx
    │       └── ResourcePanel.jsx
    └── package.json
```

---

## 🎯 What Works Right Now

✅ 40×40 dynamic grid rendering  
✅ Viewport optimization (only renders visible tiles)  
✅ Random tree placement (1-2 per tile)  
✅ Click trees to cut them down  
✅ Resource tracking (wood counter)  
✅ Pan/drag navigation  
✅ Multiple tile types (grass, dirt, forest, water)  
✅ Freepik API integration (ready for your API key)  

---

## 🔮 Next Steps

1. ✅ Get system running
2. ✅ Add your tree.png asset
3. ✅ Test tree cutting
4. 🔮 Integrate AI agents (Airia workflows)
5. 🔮 Add personality system (Fastino)
6. 🔮 Implement simulation clock
7. 🔮 Add villager behaviors

---

## 💡 Pro Tips

- **Trees not visible?** Zoom in or pan around - they're randomly placed
- **Slow performance?** Reduce grid size or tile size
- **Want more trees?** Edit `_generate_trees_for_tile()` in `grid_manager.py`
- **Custom tiles?** Add Freepik API key and call `/api/grid/initialize`

---

## 📞 Need More Help?

- **Setup issues?** → Read `SETUP.md`
- **Architecture questions?** → Read `ARCHITECTURE.md`
- **API docs?** → Read `README.md`

---

**That's it! You're ready to explore The Village!** 🌳🏡

Have fun cutting trees and gathering resources! 🪓

