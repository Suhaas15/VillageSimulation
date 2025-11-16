# 🚀 Setup Guide - The Village Project

## Prerequisites

Before starting, make sure you have:

- **Python 3.9+** installed
- **Node.js 18+** and npm installed
- **(Optional)** Freepik API key for tile generation

---

## Quick Start (Automated)

### Option 1: One-Command Launch

```bash
chmod +x start.sh
./start.sh
```

This will:
1. ✅ Check dependencies
2. 📦 Set up Python virtual environment
3. 📦 Install Python packages
4. 📦 Install npm packages
5. 🚀 Start backend on port 5000
6. 🚀 Start frontend on port 3000

Then open your browser to: **http://localhost:3000**

---

## Manual Setup

### Step 1: Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt

# Run Flask server
python app.py
```

Backend will be available at: **http://localhost:5001**

### Step 2: Frontend Setup

Open a **new terminal window**:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: **http://localhost:3000**

---

## Using Your Tree PNG Asset

1. Place your `tree.png` file in `frontend/public/` folder:
   ```
   frontend/public/tree.png
   ```

2. Update `Tree.jsx` component to use your PNG instead of emoji:

```jsx
// In frontend/src/components/Tree.jsx
// Replace the emoji with:
<img 
  src="/tree.png" 
  alt={`${type} tree`}
  style={{
    width: '48px',
    height: '48px',
    pointerEvents: 'none'
  }}
/>
```

3. Refresh the browser to see your custom trees!

---

## Optional: Freepik API Setup

To generate custom tile textures:

1. Get API key from [Freepik Developer Portal](https://www.freepik.com/api)

2. Create `.env` file in `backend/` directory:
   ```bash
   FREEPIK_API_KEY=your_actual_api_key_here
   ```

3. Update `freepik_api.py` with actual API implementation

4. Initialize tiles:
   ```bash
   curl -X POST http://localhost:5001/api/grid/initialize
   ```

---

## Testing the System

Once both servers are running:

1. **Open browser**: http://localhost:3000
2. **See the grid**: 40x40 tiles with trees
3. **Pan around**: Click and drag to explore
4. **Cut trees**: Click on any tree to gather wood
5. **Watch resources**: See wood count increase in top panel

---

## Troubleshooting

### Port already in use?

**Backend (5001):**
```bash
# Find process using port 5001
lsof -ti:5001 | xargs kill -9
```

**Frontend (3000):**
```bash
# Find process using port 3000
lsof -ti:3000 | xargs kill -9
```

### Python virtual environment issues?

```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### npm install fails?

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### CORS errors in browser?

Make sure Flask backend is running on port 5001 (not 5000, which is used by macOS AirPlay) and CORS is enabled in `app.py`.

---

## Project Structure

```
Campfire_hack_nov_25/
├── start.sh                    # Quick launch script
├── README.md                   # Main documentation
├── SETUP.md                    # This file
│
├── backend/
│   ├── app.py                  # Flask API server
│   ├── grid_manager.py         # Grid state management
│   ├── freepik_api.py          # Freepik integration
│   ├── requirements.txt        # Python dependencies
│   └── run.sh                  # Backend launch script
│
└── frontend/
    ├── src/
    │   ├── components/         # React components
    │   ├── App.jsx             # Main app
    │   └── main.jsx            # Entry point
    ├── public/                 # Static assets (put tree.png here!)
    ├── package.json            # npm dependencies
    └── vite.config.js          # Vite configuration
```

---

## Next Steps

Once you have the system running:

1. ✅ Add your custom tree.png asset
2. ✅ Explore the 40x40 grid
3. ✅ Test tree cutting and resource gathering
4. ✅ (Optional) Set up Freepik API for custom tiles
5. 🔮 Ready for Phase 2: AI Agents with Airia + Fastino

---

## Need Help?

Check the main README.md for:
- API endpoint documentation
- Feature descriptions
- Roadmap
- Tech stack details

---

**You're all set!** 🎉

The foundation is ready. When you provide your tree PNG, we can integrate it immediately!

