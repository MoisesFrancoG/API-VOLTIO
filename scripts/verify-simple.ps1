# Script simple para verificar despliegue
$domain = "voltioapi.acstree.xyz"

Write-Host "Verificando despliegue en $domain..." -ForegroundColor Green

# Test endpoint principal
Write-Host "`nProbando endpoint principal..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "https://$domain/" -TimeoutSec 10
    Write-Host "OK - Endpoint principal responde" -ForegroundColor Green
    $response | ConvertTo-Json
} catch {
    Write-Host "ERROR - Endpoint principal no responde" -ForegroundColor Red
}

# Test quick endpoint
Write-Host "`nProbando endpoint /test/quick..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "https://$domain/test/quick" -TimeoutSec 10
    Write-Host "OK - Endpoint /test/quick responde" -ForegroundColor Green
    $response | ConvertTo-Json
} catch {
    Write-Host "ERROR - Endpoint /test/quick no responde (normal si no esta desplegado)" -ForegroundColor Red
}

# Test health endpoint
Write-Host "`nProbando endpoint /test/health..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "https://$domain/test/health" -TimeoutSec 10
    Write-Host "OK - Endpoint /test/health responde" -ForegroundColor Green
    $response | ConvertTo-Json
} catch {
    Write-Host "ERROR - Endpoint /test/health no responde (normal si no esta desplegado)" -ForegroundColor Red
}

Write-Host "`nVerificacion completada" -ForegroundColor Cyan
Write-Host "URLs para verificar manualmente:"
Write-Host "- https://$domain/"
Write-Host "- https://$domain/test/quick"
Write-Host "- https://$domain/test/health"
