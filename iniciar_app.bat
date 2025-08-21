@echo off
echo ========================================
echo    SISTEMA DE GESTION DE VENTAS
echo ========================================
echo.
echo Iniciando aplicacion...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor instala Python desde https://python.org
    pause
    exit /b 1
)

REM Verificar si Flask está instalado
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Flask no está instalado. Instalando...
    pip install flask
    if errorlevel 1 (
        echo ERROR: No se pudo instalar Flask
        pause
        exit /b 1
    )
)

echo Ejecutando aplicacion...
echo.
echo IMPORTANTE:
echo - No cierres esta ventana mientras uses la aplicacion
echo - La aplicacion estara disponible en la red local
echo - Para detener, presiona Ctrl+C
echo.
python app.py

pause
