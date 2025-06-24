#!/usr/bin/env python3
"""
Quick Template Viewer
Simple command to view any generated template in browser
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path

def find_latest_template():
    """Find the most recently generated template"""
    template_dirs = [
        "templates",
        "final"
    ]
    
    latest_file = None
    latest_time = 0
    
    for dir_name in template_dirs:
        if not Path(dir_name).exists():
            continue
            
        # Look for PHP files
        for file_path in Path(dir_name).rglob("*.php"):
            if file_path.stat().st_mtime > latest_time:
                latest_time = file_path.stat().st_mtime
                latest_file = file_path
        
        # Look for HTML files in final directories
        for file_path in Path(dir_name).rglob("*.html"):
            if file_path.stat().st_mtime > latest_time:
                latest_time = file_path.stat().st_mtime
                latest_file = file_path
    
    return latest_file

def start_server(file_path, port=8080):
    """Start a simple HTTP server for the template"""
    file_dir = file_path.parent
    file_name = file_path.name
    
    print(f"🚀 Starting server for: {file_path}")
    print(f"📁 Directory: {file_dir}")
    print(f"🌐 URL: http://localhost:{port}/{file_name}")
    
    # Change to the file directory
    os.chdir(file_dir)
    
    # Start Python HTTP server
    try:
        if file_name.endswith('.php'):
            # Try PHP server first
            try:
                subprocess.run(['php', '-S', f'localhost:{port}'], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("⚠️ PHP not found, using Python server (PHP features won't work)")
                subprocess.run(['python', '-m', 'http.server', str(port)], check=True)
        else:
            # Use Python server for HTML files
            subprocess.run(['python', '-m', 'http.server', str(port)], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Server error: {e}")

def main():
    """Main function"""
    print("🔍 Template Viewer")
    print("=" * 40)
    
    # Check if specific file provided
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return
    else:
        # Find latest template
        file_path = find_latest_template()
        if not file_path:
            print("❌ No templates found!")
            print("💡 Run the pipeline first: python mcp/orchestrator.py input/example-request.md")
            return
    
    print(f"📄 Found template: {file_path}")
    
    # Determine port
    port = 8080
    if len(sys.argv) > 2:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print(f"⚠️ Invalid port '{sys.argv[2]}', using default 8080")
    
    # Open browser
    url = f"http://localhost:{port}/{file_path.name}"
    print(f"🌐 Opening: {url}")
    
    # Wait a moment then open browser
    import threading
    def open_browser():
        time.sleep(2)
        webbrowser.open(url)
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.start()
    
    # Start server
    start_server(file_path, port)

if __name__ == "__main__":
    main()
