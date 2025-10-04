#!/usr/bin/env python3
"""
BloomTrack Server Runner
Simple script to start the FastAPI server with proper configuration
"""

import uvicorn
import os
from pathlib import Path

def main():
    """Start the BloomTrack FastAPI server"""
    
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # Change to project root directory
    os.chdir(project_root)
    
    # Server configuration
    config = {
        "app": "app.main:app",
        "host": "0.0.0.0",
        "port": 8000,
        "reload": True,
        "reload_dirs": ["app"],
        "log_level": "info",
        "access_log": True
    }
    
    print("🌸 Starting BloomTrack Server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/api/docs")
    print("🔍 Alternative Docs: http://localhost:8000/api/redoc")
    print("🌍 Main Dashboard: http://localhost:8000")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        uvicorn.run(**config)
    except KeyboardInterrupt:
        print("\n🌸 BloomTrack Server stopped. Thank you for monitoring our planet's blooms!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
