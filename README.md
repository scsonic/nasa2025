# 🚀 Space Interior Designer - Nano Banana

A creative space interior design web application powered by Google Gemini 2.5 Flash (Nano Banana API).

## 🎯 Features

### Core Functionality
- **Interactive Design Canvas**: Drag and drop furniture items onto your space environment
- **AI-Powered Generation**: Use Nano Banana API to generate realistic interior designs
- **Session Management**: Each session is tracked with a unique ID for sharing
- **Dr. Bubu Assistant**: Friendly AI guide with animated text responses
- **4 Starting Environments**: Choose from Space, Moon, Mars, or Ship backgrounds

### User Workflow
1. **Select Starting Environment**: Choose one of 4 preset 800x600 environments
2. **Place Furniture**: Drag items from the scrollable furniture panel onto the canvas
3. **Add Description**: Optionally describe your design vision in text
4. **Generate**: Submit to Nano Banana API for AI-powered rendering
5. **Share**: Get a shareable session link to show your creative process

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Browser (Frontend)                       │
│  ┌──────────────┐              ┌─────────────────────────┐  │
│  │  Left Panel  │              │     Right Panel         │  │
│  │              │              │                         │  │
│  │  Dr. Bubu    │              │  Main Canvas (800x600)  │  │
│  │  Avatar      │              │  + Furniture Overlay    │  │
│  │  Message Box │              │                         │  │
│  │  Text Input  │              │  Furniture Selector     │  │
│  │  Submit Btn  │              │  (Scrollable 20 items)  │  │
│  └──────────────┘              └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (localhost:8000)                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Routes:                                             │   │
│  │  - GET  /              → index.html                  │   │
│  │  - POST /api/edit      → Image generation            │   │
│  │  - POST /api/session/create                          │   │
│  │  - GET  /api/session/{id}                            │   │
│  │  - POST /api/session/{id}/update                     │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Google Gemini 2.5 Flash API                     │
│              (gemini-2.5-flash-image-preview)                │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
nasa2025/
├── app.py                  # FastAPI backend server
├── requirements.txt        # Python dependencies
├── CLAUDE.md              # Project specifications
├── README.md              # This file
├── .env                   # Environment variables (GOOGLE_API_KEY)
├── .gitignore             # Git ignore rules
├── static/                # Static assets
│   ├── index.html         # Main UI (Space Interior Designer)
│   ├── test.html          # Original test UI
│   ├── space.png          # Starter: Space environment
│   ├── moon.png           # Starter: Moon environment
│   ├── mars.png           # Starter: Mars environment
│   ├── ship.png           # Starter: Ship environment
│   ├── dr_bubu.png        # Dr. Bubu avatar (100x100)
│   ├── construction.png   # Loading indicator
│   └── item1.png - item20.png  # Furniture items
├── input/                 # Uploaded images (gitignored)
├── result/                # Generated images (gitignored)
└── sessions/              # Session data (gitignored)
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Google AI Studio API Key

### Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   Create a `.env` file:
   ```
   GOOGLE_API_KEY=your-api-key-from-google-ai-studio
   BASE_URL=http://localhost:8000
   ```
   Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

3. **Run the server**:
   ```bash
   python app.py
   ```

4. **Open in browser**:
   Navigate to http://localhost:8000

## 🎮 How to Use

### 1. Choose Your Environment
When you first load the page, select one of four starting environments:
- **SPACE**: Deep space background
- **MOON**: Lunar surface
- **MARS**: Red planet landscape
- **SHIP**: Spaceship interior

### 2. Design Your Space
- **Drag Furniture**: Scroll through 20 furniture items and drag them onto the canvas
- **Position Items**: Drop furniture where you want it placed
- **Add Description**: Type additional design instructions in the text box
- **Visual Feedback**: Red arrows and lines show where furniture will be placed

### 3. Generate Design
- Click **Submit** when ready (button turns colorful when you have changes)
- Watch the loading overlay with construction animation
- Dr. Bubu will announce when your design is complete

### 4. Share Your Work
- Click **📤 Share Session** to copy your session link
- Share the link with others to show your creative process

## 🎨 UI Components

### Left Panel
- **Dr. Bubu Avatar**: 100x100 friendly guide
- **Message Box**: Animated text responses
- **Text Input**: Describe your design vision
- **Submit Button**: 
  - Gray when no changes
  - Colorful when ready to submit
  - Disabled during generation
- **Share Button**: Copy session link

### Right Panel
- **Main Canvas**: 800x600 display area
  - Shows current design
  - Overlays furniture placement indicators
- **Furniture Selector**: Scrollable horizontal list of 20 items
  - Drag and drop functionality
  - Hover effects for better UX

## 🔧 API Endpoints

### Frontend Routes
- `GET /` - Main application
- `GET /static/test.html` - Original test interface

### API Routes
- `POST /api/edit` - Generate design from image + prompt
- `POST /api/upload` - Upload image only
- `POST /api/edit-from-path` - Edit existing image
- `POST /api/session/create` - Create new session
- `GET /api/session/{id}` - Get session data
- `POST /api/session/{id}/update` - Update session
- `GET /health` - Health check

### Static Assets
- `/static/*` - Static files (images, HTML)
- `/images/*` - Generated result images

## 💾 Data Storage

### Session Data
Sessions are stored in `sessions/` directory as JSON files:
```json
{
  "id": "sess_abc123",
  "created_at": "2025-10-03T13:00:00",
  "history": ["/static/space.png", "/images/result1.jpg"],
  "furniture_placements": [
    {"id": "item1", "x": 400, "y": 300}
  ]
}
```

### Images
- **Input**: `input/` - Uploaded source images
- **Result**: `result/` - AI-generated images
- **Static**: `static/` - Preset starter images and UI assets

## 🎯 Key Features Explained

### Dr. Bubu Talk Animation
The `dr_talk(text)` function displays text character-by-character for a friendly, animated effect:
```javascript
function dr_talk(text) {
    // Clears message box and types text one character at a time
    // 30ms delay between characters
}
```

### Furniture Placement System
- Array stores: `{id, src, x, y}` for each placed item
- Canvas overlay draws arrows and labels
- Composite image sent to API includes placement indicators

### Submit Button State
- **Gray**: No changes made
- **Colorful**: Has text or furniture placements
- **Disabled**: During API call

### Loading Overlay
- Semi-transparent backdrop
- Animated construction icon
- "Generating... Please wait" message

## 🔒 Environment Variables

Required in `.env`:
```
GOOGLE_API_KEY=your-google-ai-studio-api-key
BASE_URL=http://localhost:8000
```

## 📝 Notes

- All placeholder images are generated programmatically
- You can replace starter images (space.png, moon.png, mars.png, ship.png) with your own 800x600 images
- Furniture items (item1-20.png) can be replaced with actual furniture icons
- Dr. Bubu avatar can be customized
- Session data persists across server restarts (stored in JSON files)

## 🐛 Troubleshooting

### Server won't start
- Check if port 8000 is available
- Verify GOOGLE_API_KEY is set in .env

### Images not generating
- Verify API key is valid
- Check API quota at Google AI Studio
- Look at server logs for errors

### Furniture not dragging
- Ensure browser supports HTML5 drag and drop
- Check browser console for JavaScript errors

## 📚 Related Documentation

- [Google Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [HTML5 Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)

## 🎉 Next Steps

You can now:
1. Replace placeholder images with real assets
2. Add more furniture items (just add item21.png, item22.png, etc.)
3. Customize Dr. Bubu's messages
4. Add more starter environments
5. Implement persistent session history viewing
6. Add undo/redo functionality
7. Export final designs

Enjoy creating amazing space interiors! 🚀✨
