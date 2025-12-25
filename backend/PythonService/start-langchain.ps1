# Start FastAPI service with LangChain Agent
# Fix encoding issues on Windows

Write-Host "Starting AI Service with LangChain Agent..." -ForegroundColor Green

# Set console to UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

# Change to service directory
Set-Location $PSScriptRoot

# Start service
Write-Host "Starting on http://localhost:8000" -ForegroundColor Cyan
python main.py
