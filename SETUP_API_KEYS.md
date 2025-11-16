# 🔑 API Keys Setup Guide

## Quick Setup

### 1. Create your `.env` file

```bash
cd backend
cat > .env << 'EOF'
# Airia AI API Key (Required for AI features)
AIRIA_API_KEY=your_airia_api_key_here

# Freepik API Key (Optional - for tile generation)
FREEPIK_API_KEY=your_freepik_api_key_here

# OpenAI API Key (Optional - for Village Oracle alternative)
OPENAI_API_KEY=your_openai_api_key_here
EOF
```

### 2. Add your Airia AI API key

Edit `backend/.env` and replace `your_airia_api_key_here` with your actual key.

---

## 🤖 Airia AI API Key

### What it's used for:

1. **🔮 Oracle Strategic AI** - High-level village strategy
2. **🏗️ Builder Tactical AI** - Specific builder actions
3. **🌍 World Analyzer** - Environment analysis and Oracle spawn

### Where to get it:

1. Visit https://airia.ai
2. Sign up / Log in
3. Get your API key from the dashboard

### Current API Endpoints:

| System | Pipeline ID | Purpose |
|--------|-------------|---------|
| **Oracle Strategic** | `31a5bde8-...` | Strategic directives |
| **Builder Tactical** | `3828632d-...` | Action commands |
| **World Analyzer** | `a019d481-...` | Environment analysis |

### Add to .env:

```bash
AIRIA_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
```

---

## 🎨 Freepik API Key (Optional)

### What it's used for:

- Generating terrain tiles (grass, dirt, water)
- Generating tree sprites
- Background removal

### Where to get it:

1. Visit https://www.freepik.com/api
2. Sign up for API access
3. Get your API key

### Add to .env:

```bash
FREEPIK_API_KEY=your_freepik_key_here
```

**Note:** System uses placeholder images if not provided.

---

## 🧙‍♂️ OpenAI API Key (Optional)

### What it's used for:

- Alternative Village Oracle system
- Villager task assignment

### Where to get it:

1. Visit https://platform.openai.com/api-keys
2. Create an API key
3. Copy the key

### Add to .env:

```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
```

**Note:** System uses rule-based fallback if not provided.

---

## 🧪 Testing Your Setup

### Test Airia AI Connection:

```bash
cd backend
source venv/bin/activate

# Set your key (temporary)
export AIRIA_API_KEY="your_key_here"

# Test Oracle Strategic API
curl --location "https://api.airia.ai/v2/PipelineExecution/31a5bde8-9c32-4038-9fa0-f347df23aa52" \
  --header "X-API-KEY: $AIRIA_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "userInput": "Builder needs guidance on what to do next",
    "asyncOutput": false
  }'

# Test Builder Tactical API
curl --location "https://api.airia.ai/v2/PipelineExecution/3828632d-7e5a-4a21-a99d-fbcb9a49b1eb" \
  --header "X-API-KEY: $AIRIA_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "userInput": "Move to position 5,10",
    "asyncOutput": false
  }'

# Test World Analyzer API
curl --location "https://api.airia.ai/v2/PipelineExecution/a019d481-6470-4b89-af5e-82c827b04c86" \
  --header "X-API-KEY: $AIRIA_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "userInput": "Analyze 20x20 grid with trees",
    "asyncOutput": false
  }'
```

### Test via Python:

```bash
cd backend
source venv/bin/activate

# Test Builder-Oracle orchestration
python test_builder_oracle.py

# Test World Analyzer
python test_oracle_environment.py

# Test Builder alone
python test_builder.py
```

---

## 🚀 Starting the System

Once you've added your API keys:

```bash
# Start backend
cd backend
source venv/bin/activate
python app.py

# In another terminal, start frontend
cd frontend
npm start
```

---

## ⚠️ Fallback Modes

All systems have fallback logic if API keys are missing:

| System | With API Key | Without API Key |
|--------|-------------|-----------------|
| **Oracle** | AI strategic decisions | Rule-based priorities |
| **Builder** | AI tactical actions | Heuristic decision tree |
| **World Analyzer** | AI clustering | Distance-based grouping |

**You can develop without API keys!** The system will use intelligent fallbacks.

---

## 🔐 Security

- **Never commit `.env` to git** (already in `.gitignore`)
- Keep API keys private
- Rotate keys if accidentally exposed
- Use environment variables in production

---

## 📊 API Key Status Check

The backend shows API key status on startup:

```
✅ Builder AI System loaded
🔑 Freepik API Key configured: Yes
🔑 OpenAI API Key configured: No (using fallback logic)
🔑 Airia API Key configured: Yes
```

---

## 🆘 Troubleshooting

### "AIRIA_API_KEY not configured"

- Check `backend/.env` exists
- Verify key is correct format
- Restart backend after adding key

### API returns 401 Unauthorized

- API key is invalid or expired
- Check key at https://airia.ai dashboard
- Regenerate if needed

### API returns 429 Rate Limited

- You've exceeded your plan's rate limit
- Wait or upgrade plan
- Use fallback mode temporarily

---

## 💡 When Do You NEED the API Key?

### ✅ You can develop WITHOUT it:
- Basic gameplay works
- Builders use rule-based logic
- World analysis uses heuristics

### ⚡ You SHOULD add it for:
- **AI-powered Builder decisions** (smarter actions)
- **Oracle strategic planning** (better village management)
- **Intelligent world analysis** (optimal spawn points)

### 🎯 You MUST add it to test:
- Builder-Oracle orchestration system
- AI directive → action pipeline
- Full autonomous agent behavior

---

## 📝 Current Status

**Ready to add your AIRIA_API_KEY when you want to:**
1. Test the new Builder-Oracle orchestration
2. Enable AI-powered strategic decisions
3. Experience full autonomous agent behavior

**System works now with fallbacks:**
- ✅ Builders can move, cut trees, build
- ✅ Oracle spawns at optimal location
- ✅ Grid renders with sprites
- ✅ All UI controls functional

---

**Need help?** Check `AIRIA_API_ENDPOINTS.md` for complete API reference.

