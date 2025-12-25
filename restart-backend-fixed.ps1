# Quick Restart Backend After Fix
# Use this to restart the Python service quickly

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  🔄 RESTARTING BACKEND AFTER FIX" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to backend
Set-Location backend/PythonService

# Check if Pillow is installed
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
$pillowInstalled = pip list | Select-String "Pillow"
if ($pillowInstalled) {
    Write-Host "✅ Pillow is installed: $pillowInstalled" -ForegroundColor Green
} else {
    Write-Host "❌ Pillow NOT found! Installing..." -ForegroundColor Red
    pip install Pillow==10.1.0
}

Write-Host ""
Write-Host "🔄 Stopping any existing Python processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "🚀 Starting backend with image support..." -ForegroundColor Green
Write-Host ""
Write-Host "Watch for these logs when uploading image:" -ForegroundColor Cyan
Write-Host "  🖼️ Image detected - using Gemini Vision API" -ForegroundColor White
Write-Host "  Image format: JPEG, Size: (width, height)" -ForegroundColor White
Write-Host "  ✅ Gemini response received" -ForegroundColor White
Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

python main.py
