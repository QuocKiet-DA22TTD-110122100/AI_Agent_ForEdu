# Setup và Test Gmail OAuth Integration
# Run this script to install dependencies and test Gmail API

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "📧 GMAIL OAUTH INTEGRATION SETUP" -ForegroundColor Yellow
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "🔍 Checking Python..." -ForegroundColor Cyan
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found! Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "`n📦 Installing dependencies..." -ForegroundColor Cyan
Write-Host "Installing nest-asyncio for async/sync support..." -ForegroundColor Gray

pip install nest-asyncio -q

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "⚠️ Some dependencies may have failed" -ForegroundColor Yellow
}

# Check .env file
Write-Host "`n🔧 Checking configuration..." -ForegroundColor Cyan

$envFile = ".\.env"
if (Test-Path $envFile) {
    $envContent = Get-Content $envFile -Raw
    
    $hasClientId = $envContent -match "GOOGLE_OAUTH_CLIENT_ID=.+"
    $hasClientSecret = $envContent -match "GOOGLE_OAUTH_CLIENT_SECRET=.+"
    $hasGmailEnabled = $envContent -match "GMAIL_API_ENABLED=true"
    
    Write-Host "  Client ID: $(if($hasClientId){'✅'}else{'❌'})" -ForegroundColor $(if($hasClientId){'Green'}else{'Red'})
    Write-Host "  Client Secret: $(if($hasClientSecret){'✅'}else{'❌'})" -ForegroundColor $(if($hasClientSecret){'Green'}else{'Red'})
    Write-Host "  Gmail Enabled: $(if($hasGmailEnabled){'✅'}else{'❌'})" -ForegroundColor $(if($hasGmailEnabled){'Green'}else{'Red'})
    
    if (!$hasClientId -or !$hasClientSecret) {
        Write-Host "`n⚠️ Missing Google OAuth credentials!" -ForegroundColor Yellow
        Write-Host "Please configure in .env file:" -ForegroundColor Gray
        Write-Host "  GOOGLE_OAUTH_CLIENT_ID=your-client-id" -ForegroundColor Gray
        Write-Host "  GOOGLE_OAUTH_CLIENT_SECRET=your-secret" -ForegroundColor Gray
    }
} else {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    exit 1
}

# Check if services are running
Write-Host "`n🔍 Checking services..." -ForegroundColor Cyan

$oauthRunning = $false
$apiRunning = $false

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8003/health" -Method GET -TimeoutSec 2 -ErrorAction SilentlyContinue
    $oauthRunning = $true
} catch {
    $oauthRunning = $false
}

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 2 -ErrorAction SilentlyContinue
    $apiRunning = $true
} catch {
    $apiRunning = $false
}

Write-Host "  OAuth Service (8003): $(if($oauthRunning){'✅ Running'}else{'❌ Not running'})" -ForegroundColor $(if($oauthRunning){'Green'}else{'Red'})
Write-Host "  API Service (8000): $(if($apiRunning){'✅ Running'}else{'❌ Not running'})" -ForegroundColor $(if($apiRunning){'Green'}else{'Red'})

# Instructions
Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "📝 NEXT STEPS" -ForegroundColor Yellow
Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host ""

if (!$oauthRunning) {
    Write-Host "1️⃣ Start OAuth Service:" -ForegroundColor Cyan
    Write-Host "   python google_oauth_service.py" -ForegroundColor Gray
    Write-Host ""
}

if (!$apiRunning) {
    Write-Host "2️⃣ Start API Service:" -ForegroundColor Cyan
    Write-Host "   python main.py" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "3️⃣ Connect Google Account:" -ForegroundColor Cyan
Write-Host "   Open: http://localhost:8003/auth/google?user_id=1" -ForegroundColor Gray
Write-Host ""

Write-Host "4️⃣ Test Gmail Integration:" -ForegroundColor Cyan
Write-Host "   python test_gmail_oauth.py" -ForegroundColor Gray
Write-Host ""

Write-Host "5️⃣ Use in Chat:" -ForegroundColor Cyan
Write-Host "   - 'Đọc email của tôi'" -ForegroundColor Gray
Write-Host "   - 'Gửi email cho example@gmail.com chủ đề Hello nội dung Test email'" -ForegroundColor Gray
Write-Host "   - 'Tìm email từ teacher@tvu.edu.vn'" -ForegroundColor Gray
Write-Host ""

Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host "📖 Full Documentation: GMAIL_OAUTH_GUIDE.md" -ForegroundColor Yellow
Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host ""

# Offer to run test
if ($oauthRunning -and $apiRunning) {
    Write-Host "🚀 Services are running!" -ForegroundColor Green
    Write-Host ""
    $runTest = Read-Host "Run Gmail OAuth test now? (y/n)"
    
    if ($runTest -eq 'y' -or $runTest -eq 'Y') {
        Write-Host ""
        Write-Host "Running test..." -ForegroundColor Cyan
        python test_gmail_oauth.py
    }
}
