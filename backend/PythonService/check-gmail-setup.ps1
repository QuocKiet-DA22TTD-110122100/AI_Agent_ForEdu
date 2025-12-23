# Setup Gmail OAuth Integration
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "            GMAIL OAUTH INTEGRATION SETUP" -ForegroundColor Yellow
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "OK Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR Python not found!" -ForegroundColor Red
    exit 1
}

# Check .env file
Write-Host ""
Write-Host "Checking configuration..." -ForegroundColor Cyan

$envFile = ".\.env"
if (Test-Path $envFile) {
    $envContent = Get-Content $envFile -Raw
    
    $hasClientId = $envContent -match "GOOGLE_OAUTH_CLIENT_ID=.+"
    $hasClientSecret = $envContent -match "GOOGLE_OAUTH_CLIENT_SECRET=.+"
    
    if ($hasClientId) {
        Write-Host "  OK Client ID configured" -ForegroundColor Green
    } else {
        Write-Host "  ERROR Client ID missing" -ForegroundColor Red
    }
    
    if ($hasClientSecret) {
        Write-Host "  OK Client Secret configured" -ForegroundColor Green
    } else {
        Write-Host "  ERROR Client Secret missing" -ForegroundColor Red
    }
    
} else {
    Write-Host "ERROR .env file not found!" -ForegroundColor Red
    exit 1
}

# Check services
Write-Host ""
Write-Host "Checking services..." -ForegroundColor Cyan

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8003/health" -Method GET -TimeoutSec 2 -ErrorAction Stop
    Write-Host "  OK OAuth Service (8003): Running" -ForegroundColor Green
    $oauthRunning = $true
} catch {
    Write-Host "  ERROR OAuth Service (8003): Not running" -ForegroundColor Red
    $oauthRunning = $false
}

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 2 -ErrorAction Stop
    Write-Host "  OK API Service (8000): Running" -ForegroundColor Green
    $apiRunning = $true
} catch {
    Write-Host "  ERROR API Service (8000): Not running" -ForegroundColor Red
    $apiRunning = $false
}

# Instructions
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
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
Write-Host "   http://localhost:8003/auth/google?user_id=1" -ForegroundColor Gray
Write-Host ""

Write-Host "4. Test Gmail:" -ForegroundColor Cyan
Write-Host "   python test_gmail_oauth.py" -ForegroundColor Gray
Write-Host ""

Write-Host "5. Chat commands:" -ForegroundColor Cyan
Write-Host "   - Doc email cua toi" -ForegroundColor Gray
Write-Host "   - Gui email cho example@gmail.com chu de Hello noi dung Test" -ForegroundColor Gray
Write-Host "   - Tim email tu teacher@tvu.edu.vn" -ForegroundColor Gray
Write-Host ""

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Documentation: GMAIL_OAUTH_GUIDE.md" -ForegroundColor Yellow
Write-Host "======================================================================" -ForegroundColor Cyan
