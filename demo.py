#!/usr/bin/env python3
"""
Demo script to show the structure of the Pastebin clone.
This can be run without dependencies to see what was built.
"""

import os

def show_file_structure():
    """Display the file structure of the Pastebin clone."""
    print("🗂️  Pastebin Clone File Structure:")
    print("=" * 50)
    
    files = [
        ("📄 main.py", "FastAPI application with all routes and API endpoints"),
        ("📄 database.py", "SQLAlchemy models and database configuration"),
        ("📄 requirements.txt", "Python dependencies"),
        ("📄 run.py", "Startup script with dependency checking"),
        ("📄 README.md", "Complete documentation and setup guide"),
        ("📁 templates/", "HTML template files"),
        ("  📄 base.html", "Base template with header, navigation, and sidebar"),
        ("  📄 index.html", "Homepage showing recent pastes"),
        ("  📄 upload.html", "Upload form for creating new pastes"),
        ("  📄 paste.html", "Paste view page with syntax highlighting"),
        ("📁 static/", "Static assets"),
        ("  📄 style.css", "Complete CSS styling matching Pastebin design"),
    ]
    
    for file_name, description in files:
        print(f"{file_name:<25} - {description}")
    
    print("\n🚀 Features Implemented:")
    print("=" * 50)
    
    features = [
        "✅ Complete database schema (id, title, content, language, etc.)",
        "✅ FastAPI backend with web routes and REST API",
        "✅ Homepage with recent pastes and sidebar",
        "✅ Upload page with form validation and language selection",
        "✅ Paste viewing with line numbers and syntax highlighting",
        "✅ Action buttons (raw, download, clone, embed, print, report)",
        "✅ Expiration system (10min, 1hour, 1day, 1week, never)",
        "✅ View counter and paste metadata",
        "✅ Responsive CSS design matching Pastebin colors",
        "✅ JavaScript functionality for interactions",
        "✅ Complete REST API for programmatic access",
        "✅ Error handling and validation",
    ]
    
    for feature in features:
        print(feature)
    
    print("\n🌐 API Endpoints:")
    print("=" * 50)
    
    endpoints = [
        ("GET /", "Homepage with recent pastes"),
        ("GET /upload", "Upload page"),
        ("POST /upload", "Create paste from web form"),
        ("GET /paste/{id}", "View paste"),
        ("GET /paste/{id}/raw", "Raw paste content"),
        ("POST /api/paste", "Create paste via API"),
        ("GET /api/paste/{id}", "Get paste data via API"),
        ("GET /api/paste/{id}/raw", "Get raw content via API"),
        ("GET /api/pastes/recent", "List recent pastes"),
    ]
    
    for endpoint, description in endpoints:
        print(f"{endpoint:<25} - {description}")
    
    print("\n📦 Tech Stack:")
    print("=" * 50)
    print("Backend: FastAPI (Python)")
    print("Database: SQLite with SQLAlchemy ORM")
    print("Frontend: HTML, CSS, JavaScript (vanilla)")
    print("Styling: Custom CSS with Pastebin color scheme")
    print("Highlighting: Highlight.js for syntax highlighting")
    
    print("\n🏃 To Run:")
    print("=" * 50)
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run: python main.py")
    print("3. Open: http://localhost:8000")

if __name__ == "__main__":
    show_file_structure()