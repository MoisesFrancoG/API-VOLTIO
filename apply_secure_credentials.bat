@echo off
echo 🛡️ APLICANDO CREDENCIALES SEGURAS - API VOLTIO
echo ================================================

echo.
echo 📋 RESUMEN DE CAMBIOS:
echo ✅ PostgreSQL: Nueva contraseña segura
echo ✅ InfluxDB: Nuevo token verificado  
echo ✅ JWT: Nueva SECRET_KEY generada
echo ✅ RabbitMQ: Credenciales actuales mantenidas
echo.

echo 🔍 Verificando archivo .env.new...
if not exist ".env.new" (
    echo ❌ Error: .env.new no encontrado
    pause
    exit /b 1
)

echo ✅ Archivo .env.new encontrado
echo.

echo 💾 Creando backup del .env actual...
if exist ".env" (
    copy ".env" ".env.backup" >nul
    echo ✅ Backup creado como .env.backup
) else (
    echo ⚠️ No existe .env actual
)

echo.
set /p confirm="🚨 ¿Aplicar las nuevas credenciales? (S/N): "
if /i "%confirm%" neq "S" (
    echo ❌ Operación cancelada
    pause
    exit /b 0
)

echo.
echo 🔄 Aplicando nuevas credenciales...
copy ".env.new" ".env" >nul
if %errorlevel% equ 0 (
    echo ✅ Credenciales aplicadas exitosamente
) else (
    echo ❌ Error al aplicar credenciales
    if exist ".env.backup" (
        echo 🔄 Restaurando backup...
        copy ".env.backup" ".env" >nul
        echo ✅ Backup restaurado
    )
    pause
    exit /b 1
)

echo.
echo 🔍 Validando nuevas credenciales...
python validate_credentials.py
if %errorlevel% equ 0 (
    echo.
    echo 🎉 ¡CREDENCIALES APLICADAS Y VALIDADAS!
    echo ✅ El sistema está listo para usar
    echo.
    echo 📁 Archivos creados:
    echo   - .env (nuevas credenciales)
    echo   - .env.backup (respaldo anterior)
    echo   - .env.new (plantilla utilizada)
    echo.
    echo 🗑️ Limpieza recomendada:
    echo   del .env.new
    echo   del validate_credentials.py
) else (
    echo.
    echo ❌ Error en validación - Restaurando backup...
    if exist ".env.backup" (
        copy ".env.backup" ".env" >nul
        echo ✅ Backup restaurado
    )
)

echo.
pause
