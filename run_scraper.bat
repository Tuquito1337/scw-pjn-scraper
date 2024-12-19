@echo off

:: Verificar si pip está instalado, si no, lo instalamos
python -m pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo pip no encontrado. Instalando pip...
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    del get-pip.py
) ELSE (
    echo pip ya está instalado.
)

:: Verificar si el entorno virtual existe, si no, lo creamos
IF NOT EXIST ".venv\" (
    echo Entorno virtual no encontrado. Creando entorno virtual...
    python -m venv .venv
) ELSE (
    echo Entorno virtual ya existe.
)

:: Activar el entorno virtual
echo Activando entorno virtual...
call .venv\Scripts\activate.bat

:: Verificar si las dependencias están instaladas
echo Verificando dependencias...
pip install --quiet --upgrade -r requirements.txt

:: Verificar si el archivo .env está configurado
IF NOT EXIST "qanlex_scraper\.env" (
    echo ¡Advertencia! El archivo .env no se encuentra. Por favor, crea un archivo .env(dentro de la carpeta qanlex_scraper) con las siguientes variables:
    echo DATABASE_HOST=localhost
    echo DATABASE_PORT=3306
    echo DATABASE_USER=root
    echo DATABASE_PASSWORD=root
    echo DATABASE_NAME=Expedientes
    echo CAP_MONSTER_APIKEY=tu_api_key_aqui
    exit /b 1
)

:: Ejecutar el scraper
echo Ejecutando scraper...
python qanlex_scraper\main.py

:: Desactivar entorno virtual después de ejecutar el scraper
deactivate
echo Scraper ejecutado y entorno virtual desactivado.

input