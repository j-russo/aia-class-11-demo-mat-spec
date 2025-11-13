# Web UI - Quick Start Guide

## Virtual Environment Setup

A virtual environment has been created to isolate dependencies. Always activate it before running the app.

### Activate Virtual Environment

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### Deactivate Virtual Environment

When you're done, deactivate with:
```bash
deactivate
```

## Running the Web UI

1. **Activate the virtual environment** (see above)

2. **Run Streamlit:**
```bash
streamlit run app.py
```

3. **Access in browser:**
   - The app will automatically open in your browser
   - Or navigate to: `http://localhost:8501`

## Features

- 📤 **Upload multiple images** (PNG, JPG, JPEG)
- 📝 **Project brief** (text area or file upload)
- ⚙️ **Options**: Sustainability and alternatives checkboxes
- 📊 **Results**: Material analysis table and specifications
- 📥 **Download**: One-click markdown download

## Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"
- Make sure the virtual environment is activated
- Reinstall: `pip install -r requirements.txt`

### Port already in use
- Streamlit will try to use port 8501
- If busy, it will try 8502, 8503, etc.
- Or specify: `streamlit run app.py --server.port 8502`

### API Key Issues
- Make sure `.env` file exists with `ANTHROPIC_API_KEY=your_key`
- The `.env` file should be in the project root

## Deployment

### Local Network Access
To share on your local network:
```bash
streamlit run app.py --server.address 0.0.0.0
```

### Streamlit Cloud (Free)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy!

