# Start Gmail API Service
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📧 GMAIL API SERVICE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting on port 8005..." -ForegroundColor Yellow
Write-Host "Swagger UI: http://localhost:8005/docs" -ForegroundColor Green
Write-Host ""

cd backend\PythonService

# Kill existing process if any
Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*gmail_api.py*"
} | Stop-Process -Force

# Start service
python gmail_api.py
