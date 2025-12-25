# Test Groq with Image Content Extraction
# Groq can now "understand" images using OCR + Image Captioning

$imagePath = "test_groq_image.jpg"

# Create test image if not exists
if (-not (Test-Path $imagePath)) {
    Add-Type -AssemblyName System.Drawing
    $bitmap = New-Object System.Drawing.Bitmap(500, 300)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    
    # White background
    $graphics.Clear([System.Drawing.Color]::White)
    
    # Draw title
    $font1 = New-Object System.Drawing.Font("Arial", 20, [System.Drawing.FontStyle]::Bold)
    $graphics.DrawString("PYTHON PROGRAMMING", $font1, [System.Drawing.Brushes]::Blue, 50, 50)
    
    # Draw code example
    $font2 = New-Object System.Drawing.Font("Courier New", 14)
    $graphics.DrawString("def hello():", $font2, [System.Drawing.Brushes]::Black, 50, 120)
    $graphics.DrawString("    print('Hello World')", $font2, [System.Drawing.Brushes]::Black, 50, 150)
    $graphics.DrawString("    return 42", $font2, [System.Drawing.Brushes]::Black, 50, 180)
    
    # Save
    $bitmap.Save($imagePath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
    $graphics.Dispose()
    $bitmap.Dispose()
    Write-Host "Created test image: $imagePath" -ForegroundColor Green
}

# Convert to base64
$imageBytes = [System.IO.File]::ReadAllBytes($imagePath)
$base64 = [Convert]::ToBase64String($imageBytes)

Write-Host "`n=== Testing Groq with Image ===" -ForegroundColor Cyan
Write-Host "Image: $imagePath" -ForegroundColor Yellow
Write-Host "Size: $($imageBytes.Length) bytes`n" -ForegroundColor Yellow

# Test with Groq
$requestBody = @{
    message = "Explain what you see in this code image. What does this Python function do?"
    ai_provider = "groq"
    model = "llama-3.3-70b-versatile"
    image_base64 = $base64
    image_mime_type = "image/jpeg"
} | ConvertTo-Json -Depth 10

Write-Host "Sending to Groq (with OCR + Image Description)..." -ForegroundColor Cyan

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/chat" `
        -Method Post -ContentType "application/json" -Body $requestBody -TimeoutSec 60
    
    Write-Host "`n" + "="*70 -ForegroundColor Green
    Write-Host "Groq Response:" -ForegroundColor Green
    Write-Host "="*70 -ForegroundColor Green
    Write-Host $response.response -ForegroundColor White
    Write-Host "="*70 -ForegroundColor Green
    Write-Host "`nModel: $($response.model)" -ForegroundColor Yellow
    
} catch {
    Write-Host "`nERROR: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails) {
        Write-Host $_.ErrorDetails.Message -ForegroundColor Red
    }
}

Write-Host "`n=== Test Complete ===" -ForegroundColor Cyan
