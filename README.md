# Proyecto de Scraping para la pagina del Poder Judicial de la Nación

Este proyecto consiste en un scraper automatizado que extrae datos de una fuente específica, resuelve captchas utilizando CapMonster, almacena los datos en una base de datos MySQL y es desplegado y gestionado en AWS. También integra GitHub Actions para despliegue continuo y configura la ejecución en horarios programados.

## Tabla de Contenidos

- [Requisitos](#requisitos)
- [Instalación](#instalación)
  - [Clonación del repositorio](#clonación-del-repositorio)
  - [Configuración del entorno](#configuración-del-entorno)
- [Uso](#uso)
  - [Ejecución local](#ejecución-local)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribución](#contribución)
- [Licencia](#licencia)

## Requisitos

Asegúrate de tener instalados los siguientes componentes:

- **Python** 3.9 o superior
- **Git**
- **MySQL** configurado para albergar los datos
- Cuenta de **CapMonster** para la resolución de captchas

## Instalación

### Clonación del repositorio

Clona el repositorio en tu máquina local:

```bash
git clone [https://github.com/tu_usuario/proyecto-scraping-aws.git](https://github.com/Tuquito1337/scw-pjn-scraper)
cd scw-pjn-scraper
```

### Configuración del entorno

Crea el archivo `.env` en el directorio del proyecto (qanlex_scraper). Copia y pega el siguiente contenido en el archivo `.env`, reemplazando los valores según sea necesario:

```bash
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=tu_contraseña
DATABASE_NAME=Expedientes
CAP_MONSTER_APIKEY=tu_api_key_aqui
```

### Configuraciones extras en `qanlex_scraper/config.py`

No modifique nada de los `os.getenv`.

```python
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

palabra_clave = "RESIDUOS"  # Cambiar según tu búsqueda

headless_option = True  # Cambiar a False si deseas ejecutar con navegador visible
```

## Uso

### Ejecución local

Mediante un script en bash podrás instalar las dependencias y ejecutar el scraper. Asegúrate de tener permisos de administrador para la instalación de dependencias.

```bash
sudo sh run_scraper.sh
```

## Estructura del Proyecto

```bash
scw-pjn-scraper
├── qanlex_scraper
│   ├── captcha_solver.py        # Lógica para resolver captchas utilizando CapMonster
│   ├── config.py                # Configuración principal del proyecto
│   ├── database
│   │   ├── db_config.py         # Configuración de la base de datos
│   │   └── models.py            # Modelos de datos para interactuar con la base de datos
│   ├── data_extractor.py        # Lógica para extraer los datos del sitio web
│   ├── main.py                  # Entrada principal para ejecutar el scraper
│   ├── models
│   │   └── informe.py           # Modelo de datos del informe extraído
│   ├── services
│   │   └── informe_service.py   # Servicios para gestionar los informes
│   └── utils.py                 # Funciones utilitarias
├── README.md                    # Este archivo
├── requirements.txt             # Lista de dependencias necesarias para el proyecto
├── run_scraper.bat              # Script para ejecutar el scraper en Windows
└── run_scraper.sh               # Script para ejecutar el scraper en sistemas Unix/Linux
```

## Contribución

¡Contribuciones son bienvenidas! Si tienes alguna sugerencia o corrección para el proyecto, puedes crear un pull request con tus cambios o abrir un issue para discutir cualquier mejora.

Para contribuir:

1. Haz un fork del proyecto.
2. Crea una nueva rama para tu contribución.
3. Realiza tus cambios y prueba que todo funcione correctamente.
4. Realiza un pull request con una descripción clara de los cambios.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Para más detalles, consulta el archivo [LICENSE](LICENSE).
