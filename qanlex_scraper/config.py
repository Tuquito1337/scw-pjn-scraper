# config.py

from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()


# Configuración de la base de datos MySQL
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "3306")
DATABASE_USER = os.getenv("DATABASE_USER", "root")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "root")
DATABASE_NAME = os.getenv("DATABASE_NAME", "Expedientes")

# Clave de API de Captcha
CAP_MONSTER_APIKEY = os.getenv("CAP_MONSTER_APIKEY", "tu_api_key_aqui")

base_url = "https://scw.pjn.gov.ar/scw/home.seam"

palabra_clave = "RESIDUOS"

headless_option = True
