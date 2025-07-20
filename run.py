#!/usr/bin/env python3
"""
Simple startup script for the Pastebin clone.
This script handles the case where we can't install dependencies.
"""

try:
    # Try to run the main application
    from main import app
    import uvicorn
    
    if __name__ == "__main__":
        print("Starting Pastebin Clone...")
        print("Open http://localhost:8000 in your browser")
        uvicorn.run(app, host="0.0.0.0", port=8000)
        
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("\nTo run this application, you need to install:")
    print("pip install fastapi uvicorn sqlalchemy jinja2 python-multipart aiofiles pygments")
    print("\nOr create a virtual environment:")
    print("python3 -m venv venv")
    print("source venv/bin/activate")
    print("pip install -r requirements.txt")
    print("python run.py")