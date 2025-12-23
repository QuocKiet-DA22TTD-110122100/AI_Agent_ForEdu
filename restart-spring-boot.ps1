# Restart Spring Boot để áp dụng thay đổi Security Config
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "🔄 RESTARTING SPRING BOOT" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""

# Find Spring Boot process
Write-Host "1️⃣  Finding Spring Boot process..." -ForegroundColor Cyan
$javaProcesses = Get-Process java -ErrorAction SilentlyContinue

if ($javaProcesses) {
    foreach ($proc in $javaProcesses) {
        # Check if it's Spring Boot (usually has "agentforedu" in command line)
        Write-Host "   Found Java process PID: $($proc.Id)" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "⚠️  Killing Java processes..." -ForegroundColor Yellow
    Stop-Process -Name java -Force -ErrorAction SilentlyContinue
    Write-Host "   ✅ Stopped" -ForegroundColor Green
    Start-Sleep -Seconds 2
} else {
    Write-Host "   No Java process found" -ForegroundColor Gray
}

Write-Host ""
Write-Host "2️⃣  Starting Spring Boot..." -ForegroundColor Cyan
Set-Location "backend\SpringService\agentforedu"

# Start Spring Boot in background
Start-Process powershell -ArgumentList "-NoExit", "-Command", "mvn spring-boot:run" -WindowStyle Normal

Write-Host "   ✅ Starting... (check new window)" -ForegroundColor Green
Write-Host ""
Write-Host "3️⃣  Waiting for Spring Boot to be ready..." -ForegroundColor Cyan

$maxAttempts = 30
$attempt = 0
$ready = $false

while ($attempt -lt $maxAttempts -and -not $ready) {
    Start-Sleep -Seconds 2
    $attempt++
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8080/swagger-ui.html" -Method GET -TimeoutSec 2 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            $ready = $true
            Write-Host "   ✅ Spring Boot is READY!" -ForegroundColor Green
        }
    } catch {
        Write-Host "   ⏳ Attempt $attempt/$maxAttempts..." -ForegroundColor Gray
    }
}

if (-not $ready) {
    Write-Host "   ⚠️  Timeout waiting for Spring Boot" -ForegroundColor Yellow
    Write-Host "   Check the Spring Boot window for errors" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "✅ DONE" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""
Write-Host "Next: Test OAuth again in the app" -ForegroundColor Cyan
