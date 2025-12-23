Write-Host "================================" -ForegroundColor Cyan
Write-Host "TEST GOOGLE CALENDAR API" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

$userId = 1

# Test 1: Get Today Events
Write-Host "`nTest 1: Getting todays events..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8004/api/google-cloud/calendar/today-events/$userId" -Method Get
    Write-Host "Success! Found $($response.count) events" -ForegroundColor Green
    $response.events | ForEach-Object { Write-Host "  - $($_.summary)" -ForegroundColor White }
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# Test 2: Create Event
Write-Host "`nTest 2: Creating new event..." -ForegroundColor Yellow
try {
    $tomorrow = (Get-Date).AddDays(1).ToString("yyyy-MM-ddT10:00:00+07:00")
    $endTime = (Get-Date).AddDays(1).ToString("yyyy-MM-ddT11:00:00+07:00")
    $body = @{
        user_id = $userId
        summary = "Test Event"
        start_time = $tomorrow
        end_time = $endTime
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "http://localhost:8004/api/google-cloud/calendar/create-event" -Method Post -Body $body -ContentType "application/json"
    Write-Host "Success! Event created: $($response.event.summary)" -ForegroundColor Green
    Write-Host "Link: $($response.event.html_link)" -ForegroundColor Blue
    $script:eventId = $response.event.id
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "TESTS COMPLETED" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
