# Script de PowerShell para verificar el despliegue
# Ejecutar con: .\scripts\verify-deployment.ps1

$domain = "voltioapi.acstree.xyz"
Write-Host "🔍 Verificando estado de despliegue en $domain..." -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Gray

function Test-Endpoint {
    param(
        [string]$Endpoint,
        [string]$Description
    )
    
    Write-Host ""
    Write-Host "🧪 Probando $Description ($Endpoint):" -ForegroundColor Yellow
    
    try {
        $url = "https://$domain$Endpoint"
        $response = Invoke-RestMethod -Uri $url -TimeoutSec 10 -ErrorAction Stop
        
        Write-Host "✅ Endpoint responde" -ForegroundColor Green
        Write-Host "📄 Respuesta:" -ForegroundColor White
        $response | ConvertTo-Json -Depth 3 | Write-Host
        
        return $response
    }
    catch {
        Write-Host "❌ Endpoint no responde o no existe aún" -ForegroundColor Red
        Write-Host "ℹ️  Esto es normal si el despliegue aún no incluye estos endpoints" -ForegroundColor Blue
        return $null
    }
}

# Verificar endpoints
$mainResponse = Test-Endpoint "/" "Endpoint principal"
$quickResponse = Test-Endpoint "/test/quick" "Verificación rápida"
$healthResponse = Test-Endpoint "/test/health" "Health check"
$deploymentResponse = Test-Endpoint "/test/deployment" "Información de despliegue"

Write-Host ""
Write-Host "==================================================" -ForegroundColor Gray
Write-Host "📊 Resumen de verificación:" -ForegroundColor Cyan

# Mostrar versión si está disponible
if ($healthResponse -and $healthResponse.version) {
    Write-Host "📦 Versión desplegada: $($healthResponse.version)" -ForegroundColor Green
} else {
    Write-Host "⚠️  No se pudo obtener la versión (endpoints de test no disponibles)" -ForegroundColor Yellow
}

# Mostrar timestamp
Write-Host "⏰ Timestamp de verificación: $(Get-Date)" -ForegroundColor White

Write-Host ""
Write-Host "🌐 URLs para verificar manualmente:" -ForegroundColor Cyan
Write-Host "- https://$domain/" -ForegroundColor White
Write-Host "- https://$domain/test/quick" -ForegroundColor White
Write-Host "- https://$domain/test/health" -ForegroundColor White
Write-Host "- https://$domain/test/deployment" -ForegroundColor White

Write-Host ""
Write-Host "💡 Para verificar en navegador, copia cualquiera de las URLs de arriba" -ForegroundColor Blue
