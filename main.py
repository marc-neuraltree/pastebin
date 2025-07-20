from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import string
import random
import uuid

from database import get_db, create_tables, Paste
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Pastebin Clone")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Create tables on startup
create_tables()

# Pydantic models for API
class PasteCreate(BaseModel):
    title: Optional[str] = None
    content: str
    language: str = "text"
    expires_in: str = "never"

class PasteResponse(BaseModel):
    id: str
    url: str

class PasteDetail(BaseModel):
    id: str
    title: Optional[str]
    content: str
    language: str
    created_at: datetime
    expires_at: Optional[datetime]
    views: int
    size_kb: float

def generate_paste_id(length=8):
    """Generate a random paste ID"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def calculate_expiration(expires_in: str) -> Optional[datetime]:
    """Calculate expiration time based on expires_in string"""
    if expires_in == "never":
        return None
    elif expires_in == "10min":
        return datetime.utcnow() + timedelta(minutes=10)
    elif expires_in == "1hour":
        return datetime.utcnow() + timedelta(hours=1)
    elif expires_in == "1day":
        return datetime.utcnow() + timedelta(days=1)
    elif expires_in == "1week":
        return datetime.utcnow() + timedelta(weeks=1)
    else:
        return None

# Web Routes
@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request, db: Session = Depends(get_db)):
    """Homepage showing recent public pastes"""
    recent_pastes = db.query(Paste).filter(
        (Paste.expires_at.is_(None)) | (Paste.expires_at > datetime.utcnow())
    ).order_by(Paste.created_at.desc()).limit(10).all()
    
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "recent_pastes": recent_pastes}
    )

@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request, db: Session = Depends(get_db)):
    """Upload page for creating new pastes"""
    # Get recent pastes for sidebar
    recent_pastes = db.query(Paste).filter(
        (Paste.expires_at.is_(None)) | (Paste.expires_at > datetime.utcnow())
    ).order_by(Paste.created_at.desc()).limit(10).all()
    
    return templates.TemplateResponse("upload.html", {"request": request, "recent_pastes": recent_pastes})

@app.post("/upload")
async def create_paste_web(
    request: Request,
    title: str = Form(None),
    content: str = Form(...),
    language: str = Form("text"),
    expires_in: str = Form("never"),
    db: Session = Depends(get_db)
):
    """Handle paste creation from web form"""
    if not content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty")
    
    paste_id = generate_paste_id()
    while db.query(Paste).filter(Paste.id == paste_id).first():
        paste_id = generate_paste_id()
    
    expires_at = calculate_expiration(expires_in)
    
    paste = Paste(
        id=paste_id,
        title=title if title else None,
        content=content,
        language=language,
        expires_at=expires_at
    )
    
    db.add(paste)
    db.commit()
    
    return RedirectResponse(url=f"/paste/{paste_id}", status_code=303)

@app.get("/paste/{paste_id}", response_class=HTMLResponse)
async def view_paste(request: Request, paste_id: str, db: Session = Depends(get_db)):
    """View a specific paste"""
    paste = db.query(Paste).filter(Paste.id == paste_id).first()
    
    if not paste:
        raise HTTPException(status_code=404, detail="Paste not found")
    
    # Check if paste has expired
    if paste.expires_at and paste.expires_at < datetime.utcnow():
        raise HTTPException(status_code=404, detail="Paste has expired")
    
    # Increment view count
    paste.views += 1
    db.commit()
    
    # Get recent pastes for sidebar
    recent_pastes = db.query(Paste).filter(
        (Paste.expires_at.is_(None)) | (Paste.expires_at > datetime.utcnow())
    ).order_by(Paste.created_at.desc()).limit(10).all()
    
    return templates.TemplateResponse(
        "paste.html", 
        {
            "request": request, 
            "paste": paste, 
            "recent_pastes": recent_pastes
        }
    )

@app.get("/paste/{paste_id}/raw", response_class=PlainTextResponse)
async def view_paste_raw(paste_id: str, db: Session = Depends(get_db)):
    """Get raw paste content"""
    paste = db.query(Paste).filter(Paste.id == paste_id).first()
    
    if not paste:
        raise HTTPException(status_code=404, detail="Paste not found")
    
    # Check if paste has expired
    if paste.expires_at and paste.expires_at < datetime.utcnow():
        raise HTTPException(status_code=404, detail="Paste has expired")
    
    return paste.content

# API Routes
@app.post("/api/paste", response_model=PasteResponse)
async def create_paste_api(paste_data: PasteCreate, db: Session = Depends(get_db)):
    """Create a new paste via API"""
    if not paste_data.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty")
    
    paste_id = generate_paste_id()
    while db.query(Paste).filter(Paste.id == paste_id).first():
        paste_id = generate_paste_id()
    
    expires_at = calculate_expiration(paste_data.expires_in)
    
    paste = Paste(
        id=paste_id,
        title=paste_data.title,
        content=paste_data.content,
        language=paste_data.language,
        expires_at=expires_at
    )
    
    db.add(paste)
    db.commit()
    
    return PasteResponse(id=paste_id, url=f"/paste/{paste_id}")

@app.get("/api/paste/{paste_id}", response_model=PasteDetail)
async def get_paste_api(paste_id: str, db: Session = Depends(get_db)):
    """Get paste details via API"""
    paste = db.query(Paste).filter(Paste.id == paste_id).first()
    
    if not paste:
        raise HTTPException(status_code=404, detail="Paste not found")
    
    # Check if paste has expired
    if paste.expires_at and paste.expires_at < datetime.utcnow():
        raise HTTPException(status_code=404, detail="Paste has expired")
    
    return PasteDetail(
        id=paste.id,
        title=paste.title,
        content=paste.content,
        language=paste.language,
        created_at=paste.created_at,
        expires_at=paste.expires_at,
        views=paste.views,
        size_kb=paste.size_kb
    )

@app.get("/api/paste/{paste_id}/raw", response_class=PlainTextResponse)
async def get_paste_raw_api(paste_id: str, db: Session = Depends(get_db)):
    """Get raw paste content via API"""
    return await view_paste_raw(paste_id, db)

@app.get("/api/pastes/recent")
async def get_recent_pastes(db: Session = Depends(get_db)):
    """Get list of recent public pastes"""
    recent_pastes = db.query(Paste).filter(
        (Paste.expires_at.is_(None)) | (Paste.expires_at > datetime.utcnow())
    ).order_by(Paste.created_at.desc()).limit(20).all()
    
    return [
        {
            "id": paste.id,
            "title": paste.title,
            "language": paste.language,
            "created_at": paste.created_at,
            "views": paste.views,
            "size_kb": paste.size_kb
        }
        for paste in recent_pastes
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)