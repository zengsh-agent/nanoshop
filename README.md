# NanoShop - AI-Powered Image Editor

<p align="center">
  <img src="https://img.shields.io/badge/NanoShop-AI%20Image%20Editor-blue" alt="NanoShop">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

A beautiful, premium AI-powered image editing web application where users can chat with their images. Describe the edits you want in natural language, and NanoShop suggests and applies the appropriate operations.

## Features

- **Chat-Based Editing**: Describe desired edits in natural language ("make it brighter", "add vintage effect")
- **Smart Suggestions**: AI analyzes your requests and suggests appropriate image operations
- **Multiple Operations**:
  - Brightness, Contrast, Saturation adjustments
  - Blur & Sharpen effects
  - Rotate & Flip (horizontal/vertical)
  - Filters: Vintage, Noir, Vivid, Sepia
  - Auto-enhance, Equalize, Autocontrast
- **Before/After Comparison**: Toggle to compare original and edited images
- **Operation History**: View, undo, or reset applied operations
- **Export**: Download edited images in PNG, JPG, or WEBP format
- **Beautiful UI**: Premium dark theme with smooth animations

## Screenshots

<p align="center">
  <img src="#" alt="NanoShop Interface" width="800">
</p>

## Quick Start

### Prerequisites

- Python 3.9+
- pip or uv

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/zengsh-agent/nanoshop.git
cd nanoshop
```

2. **Create virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### Running the Application

1. **Start the backend server** (Terminal 1):
```bash
cd backend
python main.py
# Runs on http://localhost:8000
```

2. **Start the frontend server** (Terminal 2):
```bash
cd frontend
python app.py
# Runs on http://localhost:5001
```

3. **Open in browser**:
```
http://localhost:5001
```

## Usage

1. **Upload an image**: Drag & drop or click to select an image (JPG, PNG, WEBP, BMP)
2. **Describe your edit**: Type in the chat box (e.g., "make it brighter", "add a vintage effect")
3. **Apply operations**: Click on suggested operations to apply them
4. **Compare**: Use the compare button to see before/after
5. **Export**: Click Export to download your edited image

## Project Structure

```
nanoshop/
├── backend/
│   ├── main.py              # FastAPI backend server
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── app.py               # Flask frontend server
│   ├── requirements.txt
│   ├── templates/
│   │   └── index.html       # Main HTML template
│   └── static/
│       ├── css/style.css    # Premium UI styles
│       └── js/app.js        # Frontend JavaScript
├── CLAUDE.md                # Project documentation
├── SPEC.md                  # Detailed specification
└── README.md
```

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Flask (Python) + Vanilla JavaScript
- **Image Processing**: Pillow (PIL)
- **UI**: Custom CSS with premium dark theme

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

<p align="center">Made with ❤️ by <a href="https://github.com/zengsh-agent">zengsh-agent</a></p>
