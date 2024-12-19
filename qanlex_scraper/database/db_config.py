from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from database.models import Base  # Asegúrate de importar 'Base' de donde se declara
import logging
from config import (
    DATABASE_NAME,
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
)

# Crear el motor de conexión para la base de datos
engine = create_engine(
    f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}",
    pool_pre_ping=True,  # Para verificar la conexión antes de usarla
)

# Crear la sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_database_if_not_exists():
    """Crea la base de datos si no existe."""
    try:
        connection = (
            engine.raw_connection()
        )  # Conectar sin especificar la base de datos
        with connection.cursor() as cursor:
            # Intentamos crear la base de datos si no existe
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
            connection.commit()
        logging.info(f"Base de datos '{DATABASE_NAME}' verificada/campeonada.")
    except OperationalError as e:
        logging.error(f"Error al intentar crear la base de datos: {e}")
        raise


def create_tables():
    """Crea las tablas en la base de datos."""
    try:
        # Conectar a la base de datos con la base de datos ya creada
        engine = create_engine(
            f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}",
            pool_pre_ping=True,
        )
        # Crear las tablas en la base de datos
        logging.info("Creando las tablas en la base de datos...")
        Base.metadata.create_all(bind=engine)
        logging.info("Tablas creadas exitosamente.")
    except Exception as e:
        logging.error(f"Error al crear las tablas: {e}")
        raise


# Primero creamos la base de datos si no existe
create_database_if_not_exists()

# Ahora creamos las tablas dentro de la base de datos
create_tables()
