# 🧙‍♂️ Oracle Sprite Setup

## ✅ Oracle Spawning System Implemented!

The Oracle will now spawn on a random grass tile without trees when the grid initializes.

---

## 📍 Where to Place Your Oracle GIF

Place your pixelated oracle GIF file here:

```
frontend/public/oracle.gif
```

**Full path:** `/Users/gauravhungund/Documents/Campfire_hack_nov_25/frontend/public/oracle.gif`

---

## 🎨 Oracle Sprite Requirements

### File Specifications:
- **Format**: GIF (animated or static)
- **Style**: Pixelated/pixel art
- **Recommended size**: 64x64px or similar
- **Background**: Transparent (preferred) or solid color

### Visual Guidelines:
- Should look like a wizard/sage/oracle character
- Pixel art style to match the game aesthetic
- Can be animated (walking, floating, etc.)
- Should be easily distinguishable from trees

---

## 🎮 What Happens Now

### Backend (✅ Implemented):
- Oracle spawns at a random valid location on grid initialization
- Valid location = **grass tile with no trees**
- Oracle position is tracked in grid state
- Oracle position sent to frontend via API

### Frontend (✅ Implemented):
- Oracle component displays the oracle.gif
- Oracle appears at the correct grid position
- Oracle has a glowing purple shadow effect
- Oracle scales up on hover with golden glow
- Tooltip shows "🧙‍♂️ Village Oracle" on hover
- If oracle.gif is missing, shows 🧙‍♂️ emoji as fallback

---

## 🧪 Testing

### 1. Restart Backend:
```bash
cd backend
python app.py
```

You should see:
```
🧙‍♂️ Oracle spawned at (X, Y)
```

### 2. Refresh Frontend:
```bash
# Just refresh your browser
```

The oracle will appear on a random grass tile!

---

## 🔍 Oracle Spawning Logic

```python
# In backend/grid_manager.py
def _spawn_oracle(self):
    # Find all grass tiles without trees
    valid_positions = []
    for tile in grid:
        if tile_type == 'grass' and no_trees:
            valid_positions.append(tile_position)
    
    # Spawn at random valid position
    oracle_position = random.choice(valid_positions)
```

---

## 🎨 Visual Effects

The Oracle has special visual effects:

### Normal State:
- Purple glowing shadow
- Pulsing glow animation (2s cycle)
- High z-index (appears above trees)

### Hover State:
- 15% scale increase
- Golden glow effect
- Tooltip appears above

### CSS Classes:
```css
.oracle {
  filter: drop-shadow(3px 3px 6px rgba(138, 43, 226, 0.6));
  animation: oracle-glow 2s ease-in-out infinite;
}

.oracle-hover {
  transform: scale(1.15);
  filter: drop-shadow(3px 3px 15px rgba(255, 215, 0, 0.8));
}
```

---

## 📦 Files Created/Modified

### Backend:
- ✅ `backend/grid_manager.py` - Added oracle spawning logic
  - `oracle_position` property
  - `_spawn_oracle()` method
  - Included in `get_grid_state()` response

### Frontend:
- ✅ `frontend/src/components/Oracle.jsx` - Oracle component
- ✅ `frontend/src/components/Oracle.css` - Oracle styling
- ✅ `frontend/src/components/VillageGrid.jsx` - Renders oracle on grid

---

## 🎯 Next Steps

1. **Add your oracle.gif** to `frontend/public/oracle.gif`
2. **Restart backend** to respawn oracle at new location
3. **Refresh browser** to see the oracle appear!

### Oracle GIF Recommendations:

If you don't have an oracle GIF yet, you can:
- Create one using pixel art tools (Aseprite, Piskel)
- Use AI to generate pixel art oracle
- Use a placeholder emoji (🧙‍♂️ shows automatically if no file)
- Download from pixel art asset packs

### Example Oracle Appearance:
- Wizard with robes and staff
- Glowing aura or magic effects
- Distinctive hat or mystical symbols
- Floating/hovering animation (optional)

---

## 🔄 Respawn Oracle

The oracle spawns once when the grid initializes. To respawn at a different location:

```bash
# Reset the grid (creates new oracle position)
curl -X POST http://localhost:5001/api/grid/reset
```

Then refresh your browser!

---

## 🐛 Troubleshooting

### Oracle doesn't appear:
1. Check backend logs for "🧙‍♂️ Oracle spawned at (X, Y)"
2. Check browser console for oracle position
3. Verify `frontend/public/oracle.gif` exists
4. If no GIF, you'll see 🧙‍♂️ emoji as fallback

### Oracle appears at wrong location:
- Oracle only spawns on grass tiles without trees
- If no valid positions exist, spawns at center (20, 20)

### Want to move oracle:
- Reset the grid (new random position)
- Or modify `oracle_position` manually via API

---

**Everything is ready! Just add your oracle.gif and refresh!** 🧙‍♂️✨

