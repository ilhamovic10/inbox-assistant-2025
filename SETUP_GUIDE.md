# SETUP_GUIDE.md - Complete Installation & Submission Guide

## 🎯 QUICK START - 40 MINUTES TO SUBMISSION

### Step 1: Create GitHub Repository (10 minutes)

1. Go to https://github.com/new
2. **Repository name:** inbox-assistant
3. **Description:** Multi-Agent AI System for intelligent message processing - Kaggle Capstone 2025
4. **Visibility:** PUBLIC ✅
5. **Initialize:** NO (we'll upload files)
6. Click "Create repository"

### Step 2: Upload Files to GitHub

**Using Git Command Line:**
```bash
# Navigate to your project folder
cd inbox-assistant

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Inbox Assistant multi-agent system"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/inbox-assistant.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**OR Using GitHub Web Interface:**
1. In your new repository, click "uploading an existing file"
2. Drag and drop all files
3. Commit changes

### Step 3: Repository Settings

1. Settings → General
2. Add topics: `ai-agents`, `kaggle`, `gemini`, `adk`, `multi-agent`, `nlp`
3. Verify repository is PUBLIC

### Step 4: Get Gemini API Key (5 minutes)

1. Go to https://aistudio.google.com/app/apikey
2. Click "Create API key"
3. Copy the key (starts with `AI...`)
4. Create `.env` file in your project:
   ```
   GOOGLE_API_KEY=AIza...your_actual_key_here
   ```
5. **NEVER commit .env to GitHub** (it's in .gitignore)

### Step 5: Test Locally (10 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Run demo
python examples/demo.py
```

Expected output: 4 demo messages processed with analysis

### Step 6: Submit to Kaggle (10 minutes)

1. Go to https://www.kaggle.com/competitions/agents-intensive-capstone-project
2. Click "Submit" → "Create Writeup"
3. **Title:** Inbox Assistant: AI-Powered Communication Management System
4. **Subtitle:** Multi-Agent System with 5 Specialized Agents
5. **Track:** Concierge Agents
6. **Description:** Copy from docs/KAGGLE_SUBMISSION.md (~1,450 words)
7. **Attachment:** Add your GitHub repository URL
8. Click "Submit"

---

## 📁 File Structure to Create

```
inbox-assistant/
├── agent.py                 (Main implementation)
├── config.py                (Configuration)
├── utils.py                 (Utilities)
├── requirements.txt         (Dependencies)
├── .env.example             (Environment template)
├── .gitignore               (Git ignore)
├── README.md                (Main documentation)
├── SETUP_GUIDE.md           (This file)
│
├── examples/
│   ├── sample_messages.py   (Test data)
│   └── demo.py              (Interactive demo)
│
├── tests/
│   ├── test_agents.py       (Unit tests)
│   └── evaluation.py        (Evaluation metrics)
│
└── docs/
    ├── architecture.md      (Technical details)
    └── KAGGLE_SUBMISSION.md (Kaggle writeup)
```

---

## 🔑 Kaggle Requirements Checklist

- ✅ Multi-Agent System: 5 specialized agents
- ✅ Tools: Language detection, JSON parsing, formatters
- ✅ Sessions & Memory: InMemorySessionService + InMemoryMemoryService
- ✅ Context Engineering: Structured state passing
- ✅ Agent Evaluation: Test suite with 10 messages
- ✅ Bonus: Gemini 2.0 Flash integration
- ✅ Documentation: README + Architecture + Writeup

---

## 🆘 Troubleshooting

### API Key Errors
- Check .env exists in root directory
- Verify key format: `GOOGLE_API_KEY=AIza...`
- No spaces around the key
- Test key at https://aistudio.google.com/app/apikey

### Import Errors
- Activate virtual environment: `source venv/bin/activate`
- Reinstall: `pip install -r requirements.txt --upgrade`
- Check Python version: `python --version` (need 3.9+)

### GitHub Upload Issues
- Repository must be PUBLIC
- Use web interface if command line fails
- Verify .gitignore prevents .env upload

### Demo Won't Run
- Ensure GOOGLE_API_KEY in .env
- Check internet connection
- API quota not exceeded

---

## 📞 Support

- Kaggle Discord: https://discord.com/invite/kaggle
- ADK Docs: https://google.github.io/adk-docs/
- Gemini API: https://ai.google.dev/docs

**You're ready to go! Follow the 6 steps above and you'll be submitted in 40 minutes. Good luck! 🚀**
