# Pastebin Clone

A simple Pastebin clone web application built with Python FastAPI.

## Features

- **Web Interface**: Homepage, upload page, and paste viewing
- **Database**: SQLite with SQLAlchemy ORM
- **Syntax Highlighting**: Support for multiple programming languages
- **Paste Management**: Create, view, and manage text pastes
- **Expiration**: Set expiration times (10min, 1hour, 1day, 1week, never)
- **REST API**: Full API for programmatic access
- **Responsive Design**: Works on desktop and mobile

## Tech Stack

- **Backend**: FastAPI (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Styling**: Custom CSS with Pastebin-inspired design
- **Syntax Highlighting**: Highlight.js

## Installation

### Option 1: Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Option 2: System Installation

```bash
# Install dependencies system-wide
pip install fastapi uvicorn sqlalchemy jinja2 python-multipart aiofiles pygments

# Run the application
python main.py
```

## Usage

1. Start the application:
   ```bash
   python main.py
   ```

2. Open your browser and go to: `http://localhost:8000`

3. Use the web interface:
   - Click "+ New Paste" to create a paste
   - Fill in title (optional), content, language, and expiration
   - Click "Create New Paste"
   - View your paste and use the action buttons

## API Endpoints

### Web Routes
- `GET /` - Homepage with recent pastes
- `GET /upload` - Upload page for creating new pastes  
- `POST /upload` - Handle paste creation from web form
- `GET /paste/{paste_id}` - View a specific paste
- `GET /paste/{paste_id}/raw` - Get raw paste content

### API Routes
- `POST /api/paste` - Create a new paste
- `GET /api/paste/{paste_id}` - Get paste details
- `GET /api/paste/{paste_id}/raw` - Get raw paste content
- `GET /api/pastes/recent` - Get list of recent public pastes

### API Usage Examples

**Create a paste:**
```bash
curl -X POST "http://localhost:8000/api/paste" \\
     -H "Content-Type: application/json" \\
     -d '{
       "title": "Hello World",
       "content": "print(\"Hello, World!\")",
       "language": "python",
       "expires_in": "1day"
     }'
```

**Get a paste:**
```bash
curl "http://localhost:8000/api/paste/{paste_id}"
```

**Get raw content:**
```bash
curl "http://localhost:8000/api/paste/{paste_id}/raw"
```

## Database Schema

### Pastes Table
- `id` (String, Primary Key) - Unique paste identifier
- `title` (String, Optional) - Paste title
- `content` (Text, Required) - Paste content
- `language` (String) - Programming language for syntax highlighting
- `created_at` (DateTime) - Creation timestamp
- `expires_at` (DateTime, Optional) - Expiration timestamp
- `views` (Integer) - View count

## File Structure

```
pastebin/
├── main.py              # FastAPI application
├── database.py          # Database models and configuration
├── requirements.txt     # Python dependencies
├── run.py              # Startup script
├── README.md           # This file
├── templates/          # HTML templates
│   ├── base.html       # Base template
│   ├── index.html      # Homepage
│   ├── upload.html     # Upload page
│   └── paste.html      # Paste view page
└── static/             # Static files
    └── style.css       # CSS styles
```

## Features Implemented

### Core Features
- ✅ Database schema with all required fields
- ✅ Homepage with recent pastes
- ✅ Upload page with form validation
- ✅ Paste viewing with metadata
- ✅ Syntax highlighting
- ✅ Expiration system
- ✅ View counter
- ✅ Responsive design

### API Features
- ✅ Create paste endpoint
- ✅ Get paste endpoint
- ✅ Raw content endpoint
- ✅ Recent pastes endpoint
- ✅ JSON responses
- ✅ Error handling

### UI Features
- ✅ Pastebin-inspired design
- ✅ Action buttons (raw, download, clone, etc.)
- ✅ Line numbers for code display
- ✅ Sidebar with recent pastes
- ✅ Mobile responsive layout
- ✅ Copy to clipboard functionality

## Development

To modify the application:

1. **Backend**: Edit `main.py` for routes and `database.py` for models
2. **Frontend**: Edit templates in `templates/` and styles in `static/style.css`
3. **Database**: Modify models in `database.py` and restart the application

The database is automatically created when the application starts.

## License

This project is created for educational purposes as a Pastebin clone demonstration.