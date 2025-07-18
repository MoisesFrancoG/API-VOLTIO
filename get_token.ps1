# Helper simple para pruebas de API
param(
    [string]$UserEmail = "admin@voltio.com"
)

$baseUrl = "http://localhost:8000"

Write-Host "=== API VOLTIO TEST HELPER ===" -ForegroundColor Green

# Obtener token
Write-Host "Obteniendo token para: $UserEmail" -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/debug/token?user_email=$UserEmail" -Method Get
    
    Write-Host "Token generado exitosamente:" -ForegroundColor Green
    Write-Host "Usuario: $($response.user_info.nombre)" -ForegroundColor Yellow
    Write-Host "Email: $($response.user_info.email)" -ForegroundColor Yellow
    Write-Host "" 
    Write-Host "TOKEN:" -ForegroundColor Cyan
    Write-Host $response.access_token -ForegroundColor White
    Write-Host ""
    Write-Host "Para usar en PowerShell:" -ForegroundColor Magenta
    Write-Host "`$headers = @{ 'Authorization' = 'Bearer $($response.access_token)' }" -ForegroundColor White
    
    # Probar el token
    Write-Host ""
    Write-Host "Probando token..." -ForegroundColor Cyan
    $headers = @{ "Authorization" = "Bearer $($response.access_token)" }
    $me = Invoke-RestMethod -Uri "$baseUrl/api/v1/usuarios/me" -Method Get -Headers $headers
    Write-Host "Token valido - Usuario: $($me.nombre_usuario)" -ForegroundColor Green
    
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}
