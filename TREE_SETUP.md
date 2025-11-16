# 🌳 Tree Image Setup Instructions

## ✅ Step 1: Save Your Tree Image

**Save the tree image you provided to:**
```
frontend/public/tree.png
```

### How to Save:
1. Right-click (or Ctrl+click) on the tree image you sent
2. Choose "Save Image As..."
3. Navigate to: `frontend/public/` folder
4. Name it: `tree.png`
5. Click "Save"

**Path should be:**
```
Campfire_hack_nov_25/frontend/public/tree.png
```

---

## ✅ Step 2: Configure Freepik API Key

1. **Get your Freepik API key** from: https://www.freepik.com/api

2. **Create a `.env` file** in the `backend/` folder:
   ```bash
   cd backend
   nano .env
   ```

3. **Add your API key**:
   ```
   FREEPIK_API_KEY=your_actual_freepik_api_key_here
   ```

4. **Save and exit** (Ctrl+X, then Y, then Enter)

---

## ✅ Step 3: Restart Backend

```bash
# Kill existing Flask process
lsof -ti:5001 | xargs kill -9

# Restart Flask
cd backend
source venv/bin/activate
python app.py
```

You should see:
```
🔑 Freepik API Key configured: Yes
🌳 Initializing Village Grid...
```

---

## ✅ Step 4: Generate Pixel Art Tiles

Once backend is running with API key, call:

```bash
curl -X POST http://localhost:5001/api/grid/initialize
```

This will generate **3 pixel art variations** for each tile type:
- ✅ Grass tiles (3 variations)
- ✅ Dirt tiles (3 variations)
- ✅ Forest tiles (3 variations)
- ✅ Water tiles (3 variations)

**Total: 12 AI-generated pixel art tiles!**

---

## ✅ Step 5: Refresh Browser

Refresh your browser at: http://localhost:3000

You should now see:
- ✅ **Larger tiles** (96x96 instead of 64x64)
- ✅ **Your beautiful tree image** instead of emojis
- ✅ **AI-generated pixel art tiles** (if Freepik API key is configured)

---

## 🎨 What Changed

### Tree Display
- ❌ Old: Emoji placeholders (🌳 🌲 🌴)
- ✅ New: Your pixel art tree image
- ✅ Size: 90% of tile size (scales with tile)
- ✅ Rendering: Pixelated mode (sharp edges)

### Tile Size
- ❌ Old: 64×64 pixels (small)
- ✅ New: 96×96 pixels (50% larger!)
- ✅ World size: 3,840×3,840 pixels

### Freepik Integration
- ✅ Real API implementation
- ✅ Generates 3 variations per tile type
- ✅ Optimized prompts for pixel art
- ✅ Fallback to colored placeholders if no API key
- ✅ Error handling and logging

---

## 📊 Stats

**Before:**
- Tile size: 64×64 px
- Trees: Emojis
- Tiles: CSS colors
- API: Placeholder

**After:**
- Tile size: 96×96 px (✅ 50% larger)
- Trees: Custom pixel art image
- Tiles: AI-generated pixel art (or CSS fallback)
- API: Full Freepik integration

---

## 🎮 Test It

1. ✅ Save tree.png to `frontend/public/`
2. ✅ Add Freepik API key to `backend/.env`
3. ✅ Restart backend
4. ✅ Call `/api/grid/initialize`
5. ✅ Refresh browser
6. ✅ Click trees - they should be your custom image!
7. ✅ Tiles should be AI-generated pixel art!

---

## 🐛 Troubleshooting

### Tree not showing?
- Check if `tree.png` exists in `frontend/public/`
- Hard refresh browser (Cmd+Shift+R)
- Check browser console for 404 errors

### Freepik tiles not generating?
- Check if `.env` has correct API key
- Check backend logs for errors
- Verify API key works: https://www.freepik.com/api/docs
- Falls back to colored placeholders if API fails

### Tiles too big/small?
Change `TILE_SIZE` in:
```javascript
// frontend/src/components/VillageGrid.jsx
const TILE_SIZE = 96  // Change to 64, 128, etc.
```

---

**Ready to go!** 🚀

Save your tree image and restart the backend to see the changes!

