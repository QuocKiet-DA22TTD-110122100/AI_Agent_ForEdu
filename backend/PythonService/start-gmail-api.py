"""
Quick start Gmail API service
"""
import subprocess
import sys

print("""
╔══════════════════════════════════════════════════════════╗
║          📧 GMAIL API SERVICE - SWAGGER TEST            ║
╔══════════════════════════════════════════════════════════╗

Starting on port 8005...
Swagger UI: http://localhost:8005/docs

""")

try:
    subprocess.run([
        sys.executable, 
        "gmail_api.py"
    ])
except KeyboardInterrupt:
    print("\n👋 Service stopped")
