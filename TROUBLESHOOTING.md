# 🔧 Troubleshooting - CORS Issue Fixed!

## ✅ Issue Resolved: macOS Port 5000 Conflict

### What Happened
The CORS error you saw was because **macOS uses port 5000 for AirPlay Receiver** by default. Flask couldn't bind to that port.

### What Was Fixed
- Changed Flask backend from port **5000** → **5001**
- Updated frontend API URL to use port **5001**
- Updated all documentation
- Backend is now running successfully! ✅

---

## 🚀 Current Status

### Backend
✅ **Running on port 5001**
```bash
curl http://localhost:5001/api/health
# Response: {"status": "healthy", "service": "village-backend"}
```

### Grid Initialized
✅ **1,669 trees generated** across the 40×40 grid!

---

## 🎯 What You Need to Do

### Refresh Your Browser!
The frontend is looking for the backend on the correct port now (**5001**).

Simply **refresh your browser** at:
```
http://localhost:3000
```

The CORS error should be **gone** and you should see:
- ✅ 40×40 tile grid
- ✅ Trees scattered around (🌳 🌲 🌴)
- ✅ Resource counter at top
- ✅ Ability to click trees and gather wood!

---

## 🔍 Verify Backend is Running

```bash
# Check if Flask is running
curl http://localhost:5001/api/health

# Check resources
curl http://localhost:5001/api/resources

# Check grid (returns lots of data!)
curl http://localhost:5001/api/grid | python3 -m json.tool | head -50
```

---

## 🛑 Stop Backend (If Needed)

```bash
# Find and kill Flask process
lsof -ti:5001 | xargs kill -9
```

---

## 🔄 Restart Backend

```bash
cd backend
source venv/bin/activate
python app.py
```

You should see:
```
🌳 Initializing Village Grid...
Generating 40x40 grid...
✅ Grid initialized with 1669 trees
✅ Grid initialized: 40x40
 * Running on http://127.0.0.1:5001
```

---

## 📝 Other Common Issues

### Frontend not updating?
```bash
# Hard refresh browser
Cmd + Shift + R (macOS)
Ctrl + Shift + R (Windows/Linux)
```

### Dependencies missing?
```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Port conflicts?
```bash
# Backend (5001)
lsof -ti:5001 | xargs kill -9

# Frontend (3000)
lsof -ti:3000 | xargs kill -9
```

---

## 🎉 Success Indicators

You'll know everything is working when:

1. ✅ Backend terminal shows: `Running on http://127.0.0.1:5001`
2. ✅ `curl http://localhost:5001/api/health` returns JSON
3. ✅ Browser shows purple gradient with grid
4. ✅ Trees are visible (🌳 🌲 🌴)
5. ✅ Clicking trees makes them disappear
6. ✅ Wood counter increases
7. ✅ **No CORS errors in browser console!**

---

## 💡 Why Port 5001?

macOS Monterey and later use **port 5000** for the AirPlay Receiver service by default. Options:

1. ✅ **Use port 5001** (what we did - easiest!)
2. Disable AirPlay Receiver in System Preferences
3. Change AirPlay port manually

We chose option 1 for maximum compatibility.

---

## 📞 Still Having Issues?

Check:
1. Both backend AND frontend are running
2. Backend is on port **5001** (not 5000)
3. Frontend is looking at the correct API URL
4. Browser console for any other errors
5. Backend logs: `backend/flask.log`

---

**Status**: ✅ **FIXED AND RUNNING**

Backend PID: Check with `lsof -ti:5001`

Last tested: Working perfectly! 🎉

