# Setup Gmail OAuth Integration
Write-Host "======================================================================"  -ForegroundColor Cyan
Write-Host "            GMAIL OAUTH INTEGRATION SETUP" -ForegroundColor Yellow
Write-Host "======================================================================"  -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python..." -ForegroundColor Cyan
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python not found! Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check .env file
Write-Host "`nChecking configuration..." -ForegroundColor Cyan

$envFile = ".\.env"
if (Test-Path $envFile) {
    $envContent = Get-Content $envFile -Raw
    
    $hasClientId = $envContent -match "GOOGLE_OAUTH_CLIENT_ID=.+"
    $hasClientSecret = $envContent -match "GOOGLE_OAUTH_CLIENT_SECRET=.+"
    
    if ($hasClientId) {
        Write-Host "  ✓ Client ID configured" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Client ID missing" -ForegroundColor Red
    }
    
    if ($hasClientSecret) {
        Write-Host "  ✓ Client Secret configured" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Client Secret missing" -ForegroundColor Red
    }
    
} else {
    Write-Host "✗ .env file not found!" -ForegroundColor Red
    exit 1
}

# Check services
Write-Host "`nChecking services..." -ForegroundColor Cyan

$oauthRunning = $false
$apiRunning = $false

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8003/health" -Method GET -TimeoutSec 2 -ErrorAction Stop
    $oauthRunning = $true
    Write-Host "  ✓ OAuth Service (8003): Running" -ForegroundColor Green
} catch {
    Write-Host "  ✗ OAuth Service (8003): Not running" -ForegroundColor Red
}

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 2 -ErrorAction Stop
    $apiRunning = $true
    Write-Host "  ✓ API Service (8000): Running" -ForegroundColor Green
} catch {
    Write-Host "  ✗ API Service (8000): Not running" -ForegroundColor Red
}

# Instructions
Write-Host "`n======================================================================" -ForegroundColor Cyan
Write-Host "                         NEXT STEPS" -ForegroundColor Yellow
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

if (-not $oauthRunning) {
    Write-Host "1. Start OAuth Service:" -ForegroundColor Cyan
    Write-Host "   python google_oauth_service.py" -ForegroundColor Gray
    Write-Host ""
}

if (-not $apiRunning) {
    Write-Host "2. Start API Service:" -ForegroundColor Cyan
    Write-Host "   python main.py" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "3. Connect Google Account:" -ForegroundColor Cyan
Write-Host "   Open: http://localhost:8003/auth/google?user_id=1" -ForegroundColor Gray
Write-Host ""

Write-Host "4. Test Gmail Integration:" -ForegroundColor Cyan
Write-Host "   python test_gmail_oauth.py" -ForegroundColor Gray
Write-Host ""

Write-Host "5. Use in Chat:" -ForegroundColor Cyan
Write-Host "   - Đọc email của tôi" -ForegroundColor Gray
Write-Host "   - Gửi email cho example@gmail.com chủ đề Hello nội dung Test" -ForegroundColor Gray
Write-Host "   - Tìm email từ teacher@tvu.edu.vn" -ForegroundColor Gray
Write-Host ""

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Full Documentation: GMAIL_OAUTH_GUIDE.md" -ForegroundColor Yellow
Write-Host "======================================================================" -ForegroundColor Cyan
