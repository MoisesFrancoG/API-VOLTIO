# 🔧 API VOLTIO - Generador de Tokens de Prueba (PowerShell)
# =========================================================

param(
    [string]$Environment = "prod",  # local o prod
    [switch]$All,                   # Obtener todos los tokens
    [string]$TestToken             # Probar un token específico
)

# URLs de la API
$ApiUrls = @{
    "local" = "http://localhost:8000"
    "prod" = "https://voltioapi.acstree.xyz"
}

$BaseUrl = $ApiUrls[$Environment]

Write-Host "🚀 API VOLTIO - Generador de Tokens" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray
Write-Host "🌐 Ambiente: $($Environment.ToUpper())" -ForegroundColor Yellow
Write-Host "🔗 URL: $BaseUrl" -ForegroundColor Yellow
Write-Host "=" * 50 -ForegroundColor Gray

try {
    if ($TestToken) {
        # Probar token específico
        Write-Host "`n🧪 PROBANDO TOKEN:" -ForegroundColor Magenta
        
        $headers = @{ 
            "Authorization" = "Bearer $TestToken"
        }
        
        $response = Invoke-RestMethod -Uri "$BaseUrl/api/v1/users/me" -Headers $headers -Method Get
        
        Write-Host "✅ Token válido" -ForegroundColor Green
        $response | ConvertTo-Json -Depth 3 | Write-Host
        
    } elseif ($All) {
        # Obtener todos los tokens
        Write-Host "`n👥 OBTENIENDO TOKENS DE TODOS LOS USUARIOS:" -ForegroundColor Magenta
        
        $response = Invoke-RestMethod -Uri "$BaseUrl/debug/test-tokens" -Method Get
        
        if ($response.error) {
            Write-Host "❌ ERROR: $($response.error)" -ForegroundColor Red
            exit 1
        }
        
        $response | ConvertTo-Json -Depth 4 | Write-Host
        
        # Mostrar ejemplos de uso
        Write-Host "`n💡 EJEMPLOS DE USO:" -ForegroundColor Yellow
        Write-Host "=" * 30 -ForegroundColor Gray
        
        foreach ($email in $response.tokens.PSObject.Properties.Name) {
            $tokenData = $response.tokens.$email
            $token = $tokenData.access_token
            $role = $tokenData.user.role_name
            
            Write-Host "`n🔑 $email ($role):" -ForegroundColor Cyan
            Write-Host "Token: $($token.Substring(0, 20))..." -ForegroundColor Gray
            Write-Host "Ejemplo curl:" -ForegroundColor Gray
            Write-Host "curl -H 'Authorization: Bearer $token' \\" -ForegroundColor White
            Write-Host "     $BaseUrl/api/v1/users/me" -ForegroundColor White
        }
        
    } else {
        # Obtener token de SuperAdmin
        Write-Host "`n🔐 OBTENIENDO TOKEN DE SUPERADMIN:" -ForegroundColor Magenta
        
        $response = Invoke-RestMethod -Uri "$BaseUrl/debug/get-token" -Method Get
        
        if ($response.error) {
            Write-Host "❌ ERROR: $($response.error)" -ForegroundColor Red
            exit 1
        }
        
        $response | ConvertTo-Json -Depth 3 | Write-Host
        
        # Mostrar ejemplo de uso
        $token = $response.access_token
        Write-Host "`n💡 EJEMPLO DE USO:" -ForegroundColor Yellow
        Write-Host "=" * 30 -ForegroundColor Gray
        Write-Host "Token: $($token.Substring(0, 20))..." -ForegroundColor Gray
        Write-Host "curl -H 'Authorization: Bearer $token' \\" -ForegroundColor White
        Write-Host "     $BaseUrl/api/v1/users/me" -ForegroundColor White
    }
    
} catch {
    Write-Host "❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode.Value__
        Write-Host "HTTP Status: $statusCode" -ForegroundColor Red
    }
}

Write-Host "`n✅ Proceso completado" -ForegroundColor Green
