# NanoShop - AI-Powered Image Editor

## Project Overview

NanoShop is a beautiful, premium-feeling AI-powered image editing web application where users can chat with their images. The AI analyzes the image and conversation, then suggests and applies appropriate editing operations (saturation, masks, filters, brightness, contrast, etc.) to achieve the desired result.

## Project Structure

```
nanops/
├── SPEC.md                 # Detailed project specification
├── CLAUDE.md               # This file - project documentation
├── .env.example            # Environment variables template
├── app.py                  # Main entry point (run both servers)
├── backend/
│   ├── main.py             # FastAPI backend server
│   └── requirements.txt    # Python dependencies
└── frontend/
    ├── app.py              # Flask frontend server
    ├── requirements.txt     # Python dependencies
    ├── templates/
    │   └── index.html      # Main HTML template
    └── static/
        ├── css/
        │   └── style.css   # Premium UI styles
        └── js/
            └── app.js      # Frontend JavaScript
```

## Tech Stack

- **Backend**: FastAPI (Python) with Uvicorn
- **Frontend**: Flask (Python) serving HTML/CSS/JS
- **AI**: Anthropic Claude API for natural language understanding
- **Image Processing**: Pillow (PIL) and NumPy

## Commands

### Setup

1. **Install dependencies**:
   ```bash
   cd backend && pip install -r requirements.txt
   cd ../frontend && pip install -r requirements.txt
   ```

2. **Set environment variable**:
   ```bash
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

### Running the Application

**Option 1 - Separate terminals**:
```bash
# Terminal 1 - Backend
cd backend
python main.py
# Runs on http://localhost:8000

# Terminal 2 - Frontend
cd frontend
python app.py
# Runs on http://localhost:5000
```

**Option 2 - Use main app**:
```bash
python app.py
# Follow prompts to install deps or start servers
```

### Access

Open http://localhost:5000 in your browser.

## Features

1. **Image Upload**: Drag & drop or click to upload (JPG, PNG, WEBP, BMP)
2. **AI Chat Interface**: Natural language conversation about desired edits
3. **Smart Operations**:
   - Brightness, Contrast, Saturation adjustments
   - Blur/Sharpen effects
   - Rotate, Flip (horizontal/vertical)
   - Filters: Vintage, Noir, Vivid, Sepia
   - Auto-enhance, Equalize, Autocontrast
4. **Operation Management**: View, reorder, and undo operations
5. **Export**: Download in PNG, JPG, or WEBP format
6. **Before/After Comparison**: Toggle to compare original and edited

## UI/UX Design

- **Theme**: Dark navy with coral accent (#E94560)
- **Typography**: Outfit (headings), DM Sans (body)
- **Effects**: Glassmorphism, smooth animations, gradient accents
- **Responsive**: Works on desktop, tablet, and mobile

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload` | Upload image |
| POST | `/api/chat` | Chat with AI |
| POST | `/api/apply` | Apply operation |
| POST | `/api/preview` | Preview operation |
| POST | `/api/undo` | Undo last operation |
| POST | `/api/reset` | Reset to original |
| GET | `/api/image/{session_id}` | Get image state |
| POST | `/api/export` | Export image |

## Conventions

- **Python**: PEP 8 style, type hints for functions
- **Frontend**: Vanilla JavaScript (no frameworks)
- **CSS**: CSS variables for theming
- **API**: RESTful, JSON responses
- **State**: In-memory sessions (use Redis in production)
