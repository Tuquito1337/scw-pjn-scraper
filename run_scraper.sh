#!/bin/bash

# Verificar si pip está instalado, si no, lo instalamos
if ! python3 -m pip --version &>/dev/null; then
    echo "pip no encontrado. Instalando pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
else
    echo "pip ya está instalado."
fi

# Verificar si el entorno virtual existe, si no, lo creamos
if [ ! -d ".venv" ]; then
    echo "Entorno virtual no encontrado. Creando entorno virtual..."
    python3 -m venv .venv
else
    echo "Entorno virtual ya existe."
fi

# Activar el entorno virtual
echo "Activando entorno virtual..."
source .venv/bin/activate

# Verificar si las dependencias están instaladas
echo "Verificando dependencias..."
pip install --quiet --upgrade -r requirements.txt

# Verificar si el archivo .env está configurado
if [ ! -f "qanlex_scraper/.env" ]; then
    echo "¡Advertencia! El archivo .env no se encuentra. Por favor, crea un archivo .env(dentro de la carpeta qanlex_scraper) con las siguientes variables:"
    echo "DATABASE_HOST=localhost"
    echo "DATABASE_PORT=3306"
    echo "DATABASE_USER=root"
    echo "DATABASE_PASSWORD=root"
    echo "DATABASE_NAME=Expedientes"
    echo "CAP_MONSTER_APIKEY=tu_api_key_aqui"
    exit 1
fi

# Ejecutar el scraper
echo "Ejecutando scraper..."
python qanlex_scraper/main.py

# Desactivar entorno virtual después de ejecutar el scraper
deactivate
echo "Scraper ejecutado y entorno virtual desactivado."
