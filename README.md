# 🚀 Space Interior Designer - Nano Banana

A creative space interior design web application powered by Google Gemini 2.5 Flash.

## ⚡ Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 3. Run locally
python app.py

# 4. Open browser
open http://localhost:8000
```

## 🎯 Features

### Core Functionality
- **Interactive Design Canvas**: Drag and drop furniture items onto your space environment
- **AI-Powered Generation**: Use Gemini 2.5 Flash to generate realistic interior designs
- **Session Management**: Auto-generated session ID tracks your creative process
- **Share & Slideshow**: Share your design history with animated slideshow (500ms transitions)
- **Dual Storage Mode**: Local storage (default) or Google Cloud Storage
- **Dr. Bubu Assistant**: Friendly AI guide with animated text responses
- **4 Starting Environments**: Choose from Space, Moon, Mars, or Ship backgrounds

### User Workflow
1. **Select Starting Environment**: Choose one of 4 preset 800x600 environments
2. **Place Furniture**: Drag items from the scrollable furniture panel onto the canvas
3. **Add Description**: Optionally describe your design vision in text
4. **Generate**: Submit to Gemini API for AI-powered rendering
5. **Share**: Click share button to get slideshow link

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
│  │  - GET  /share/{id}    → share.html (slideshow)      │   │
│  │  - POST /api/edit      → Image generation + session  │   │
│  │  - GET  /api/session/{id}                            │   │
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
├── app.yaml                # Google App Engine config
├── requirements.txt        # Python dependencies
├── CLAUDE.md              # Project specifications
├── README.md              # This file
├── .env                   # Environment variables (not in git)
├── .env.example            # Environment template
├── .gitignore             # Git ignore rules
├── static/                # Static assets
│   ├── index.html         # Main UI
│   ├── share.html         # Share page with slideshow
│   └── img/               # Images (starters, furniture, etc.)
├── input/                 # Uploaded images (local mode)
├── result/                # Generated images (local mode)
└── sessions/              # Session JSON (local + backup)
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
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your API key:
   ```env
   GOOGLE_API_KEY=your-api-key-from-google-ai-studio
   USE_GCS=false  # Use local storage (default)
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
- Click **📤 Share** button (top right)
- Link automatically copied to clipboard
- Opens slideshow in new tab
- Share URL format: `http://localhost:8000/share/sess_xxx`
- **Slideshow features**:
  - Auto-play with 500ms transitions
  - Fade in/out effects
  - Navigation arrows and keyboard controls (←/→/Space)
  - Semi-transparent play button (bottom right)

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
- `POST /api/edit` - Generate design (includes session_id)
- `GET /api/session/{id}` - Get session data
- `GET /health` - Health check

### Frontend Routes
- `GET /` - Main application (index.html)
- `GET /share/{session_id}` - Share page with slideshow

### Static Assets
- `/static/*` - Static files (images, HTML)
- `/images/*` - Generated result images (local mode)

## 💾 Storage Modes

### Local Storage (USE_GCS=false) ⭐ Default

**Configuration**:
```env
USE_GCS=false
BASE_URL=http://localhost:8000
```

**Storage**:
- Images: `./result/`
- Sessions: `./sessions/`
- URL format: `http://localhost:8000/images/uuid.jpg`

**Pros**: Free, fast, no GCP setup needed  
**Cons**: Local only, can't share across devices

### GCS Storage (USE_GCS=true)

**Configuration**:
```env
USE_GCS=true
GCS_BUCKET_NAME=team-bubu
BASE_URL=http://localhost:8000
```

**Storage**:
- Images: `gs://team-bubu/result/` + local backup
- Sessions: `gs://team-bubu/json/` + local backup
- URL format: `https://storage.googleapis.com/team-bubu/result/uuid.jpg`

**Pros**: Public URLs, permanent storage, shareable  
**Cons**: Requires GCP setup, storage costs (~$0.02/GB/month)

**Setup GCS**:
```bash
# 1. Authenticate
gcloud auth application-default login

# 2. Set bucket public
gsutil iam ch allUsers:objectViewer gs://team-bubu

# 3. Update .env
USE_GCS=true
```

### Session Data Format
```json
{
  "id": "sess_1728024000000_abc123",
  "created_at": "2025-10-04T15:00:00",
  "updated_at": "2025-10-04T15:05:00",
  "history": [
    "https://storage.googleapis.com/team-bubu/result/uuid1.jpg",
    "https://storage.googleapis.com/team-bubu/result/uuid2.jpg"
  ]
}
```

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

Create `.env` file (copy from `.env.example`):

```env
# Required
GOOGLE_API_KEY=your-gemini-api-key

# Storage mode (false=local, true=GCS)
USE_GCS=false

# GCS bucket (only if USE_GCS=true)
GCS_BUCKET_NAME=team-bubu

# Base URL
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

### Share page not loading
- Verify session ID is correct
- Check if session JSON exists
- Ensure history array has valid image URLs

### GCS errors
- Run `gcloud auth application-default login`
- Verify bucket name matches `.env`
- Check bucket is public: `gsutil iam get gs://team-bubu`

## 🚀 Deployment to App Engine

### Prerequisites
- GCP Project: `team-bubu`
- Bucket: `gs://team-bubu` (public access)
- App Engine enabled

### Deploy Steps

```bash
# 1. Set project
gcloud config set project team-bubu

# 2. Set API key (use Secret Manager)
gcloud services enable secretmanager.googleapis.com
echo -n "YOUR_API_KEY" | gcloud secrets create GOOGLE_API_KEY --data-file=-

# 3. Grant access
gcloud secrets add-iam-policy-binding GOOGLE_API_KEY \
  --member=serviceAccount:team-bubu@appspot.gserviceaccount.com \
  --role=roles/secretmanager.secretAccessor

# 4. Deploy
gcloud app deploy

# 5. Open
gcloud app browse
```

### app.yaml Configuration

```yaml
runtime: python312
instance_class: F2

env_variables:
  USE_GCS: "true"
  GCS_BUCKET_NAME: "team-bubu"
  BASE_URL: "https://team-bubu.appspot.com"
  GOOGLE_API_KEY: ${GOOGLE_API_KEY}

automatic_scaling:
  min_instances: 0  # Save costs
  max_instances: 10
```

### Monitor

```bash
# View logs
gcloud app logs tail -s default

# Check versions
gcloud app versions list
```

## 📚 Related Documentation

- [Google Gemini API](https://ai.google.dev/gemini-api/docs)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Google Cloud Storage](https://cloud.google.com/storage/docs)
- [App Engine](https://cloud.google.com/appengine/docs)

## 💡 Tips & Best Practices

### Development
- Use `USE_GCS=false` for faster local development
- Test with small images first
- Check logs for session updates

### Production
- Use `USE_GCS=true` for shareable URLs
- Set `min_instances: 0` in app.yaml to save costs
- Monitor GCS storage usage
- Set up lifecycle policies to auto-delete old files

### Customization
- Replace starter images in `static/img/` (recommended: 1184x864)
- Add more furniture: `item21.png`, `item22.png`, etc.
- Modify slideshow timing in `share.html` (default: 500ms)
- Customize Dr. Bubu messages

## 🎉 Next Steps

1. **Local Development**: Start with `USE_GCS=false`
2. **Test Features**: Generate images, test share functionality
3. **Enable GCS**: Switch to `USE_GCS=true` for public sharing
4. **Deploy**: Use `gcloud app deploy` for production
5. **Monitor**: Check logs and costs regularly

Enjoy creating amazing space interiors! 🚀✨
