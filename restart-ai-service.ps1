# 🔄 Restart AI Service sau khi fix Google Cloud port
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "🔄 RESTARTING AI SERVICE (Port 8000)" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""

# Kill existing AI service
Write-Host "1️⃣  Stopping old AI service..." -ForegroundColor Cyan
$port8000 = netstat -ano | findstr ":8000" | ForEach-Object { 
    if ($_ -match '\s+(\d+)$') { $matches[1] } 
} | Select-Object -First 1

if ($port8000) {
    Write-Host "   Found PID: $port8000" -ForegroundColor Gray
    taskkill /PID $port8000 /F 2>$null
    Write-Host "   ✅ Stopped" -ForegroundColor Green
    Start-Sleep -Seconds 2
} else {
    Write-Host "   No service running on port 8000" -ForegroundColor Gray
}

Write-Host ""
Write-Host "2️⃣  Starting AI service..." -ForegroundColor Cyan
Set-Location "backend\PythonService"

# Start in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python main.py" -WindowStyle Normal

Write-Host "   ✅ Started in new window" -ForegroundColor Green

Write-Host ""
Write-Host "3️⃣  Waiting for service to be ready..." -ForegroundColor Cyan

$maxAttempts = 15
$attempt = 0
$ready = $false

while ($attempt -lt $maxAttempts -and -not $ready) {
    Start-Sleep -Seconds 2
    $attempt++
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/" -Method GET -TimeoutSec 2 -ErrorAction Stop
        if ($response.status -eq "running") {
            $ready = $true
            Write-Host "   ✅ AI Service is READY!" -ForegroundColor Green
            Write-Host "   Version: $($response.version)" -ForegroundColor Gray
        }
    } catch {
        Write-Host "   ⏳ Attempt $attempt/$maxAttempts..." -ForegroundColor Gray
    }
}

if (-not $ready) {
    Write-Host "   ⚠️  Service may still be starting..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "✅ DONE - AI Service Restarted" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""
Write-Host "🎯 Now you can test Google Cloud features in chatbox!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Try these commands:" -ForegroundColor Yellow
Write-Host '  - "Dịch sang tiếng Anh: Xin chào"' -ForegroundColor White
Write-Host '  - "Phân tích cảm xúc: This is amazing!"' -ForegroundColor White
Write-Host '  - "Phân tích ảnh này: [URL]"' -ForegroundColor White
