# EVE AI Setup Guide

**Created by:** Hassan Muzenda

## ⚠️ IMPORTANT: Adding Your API Key

### Step 1: Get Your API Key
1. Go to https://platform.openai.com/api-keys
2. Create a **new** secret key (make sure to revoke any leaked ones!)
3. Copy the key (starts with `sk-...`)

### Step 2: Add Key to Config
Open this file: **`eve/backend/config.json`**

Find this section:
```json
"default_ai": {
    "id": "default",
    "name": "OpenAI GPT-4",
    "type": "openai",
    "endpoint": "https://api.openai.com/v1/chat/completions",
    "model": "gpt-4",
    "api_key": "YOUR_API_KEY_HERE",  <-- REPLACE THIS
    "enabled": true
},
```

Replace `"YOUR_API_KEY_HERE"` with your actual key:
```json
"api_key": "sk-proj-your-new-key-here",
```

### Step 3: Save and Run!

## 🚀 Running EVE

```bash
# Install dependencies
cd eve/backend
pip install -r requirements.txt

# Start the server
python server.py
```

## 🌐 Access EVE

- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs
- **Health:** http://localhost:8000/health

## 🌍 Supported Languages

EVE supports 14 languages:
- English (en), Shona (sn), Japanese (ja), Korean (ko), Russian (ru)
- Chinese (zh), Spanish (es), French (fr), German (de), Portuguese (pt)
- Arabic (ar), Hindi (hi), Swahili (sw), Zulu (zu)

## 📁 Project Files

```
eve/backend/
├── server.py          # Main API server
├── config.json        # ⚠️ API KEY GOES HERE
├── ai_engine.py      # AI reasoning
├── security.py       # Pen testing tools
├── plugins.py        # Custom AI plugins
├── voice.py          # Voice chat
├── language.py       # Multi-language
├── multimodal.py     # Text, voice, image I/O
├── tasks.py          # Task primitives
├── safety.py         # Safety & compliance
├── connectors.py     # External integrations
├── reasoning.py      # Planning engine
├── memory.py         # Memory system
└── requirements.txt  # Dependencies
```

## ⚠️ Security Tips

1. **Never share your API key publicly**
2. **Revoke leaked keys immediately**
3. **Use environment variables for production**
4. **Keep your key private!**

---

**EVE AI v4.0** - Created by Hassan Muzenda
