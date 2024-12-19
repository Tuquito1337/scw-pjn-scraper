from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.db_config import SessionLocal
from database.models import Informe, FechaRelevante
from models.informe import Informe as InformeClass
import logging

# Configuración del logger
logger = logging.getLogger(__name__)


def find_existing_informe(db: Session, expediente: str) -> Informe:
    """Busca un informe existente por expediente."""
    return db.query(Informe).filter_by(expediente=expediente).first()


def update_informe(existing_informe: Informe, new_data: InformeClass):
    """Actualiza los campos de un informe existente con datos nuevos."""
    fields_to_update = [
        "jurisdiccion",
        "situacion_actual",
        "dependencia",
        "demandante",
        "demandado",
        "caratula",
        "tipo_demanda",
        "juzgado",
    ]
    for field in fields_to_update:
        new_value = getattr(new_data, field, None)
        if new_value:
            setattr(existing_informe, field, new_value)


def add_or_update_fechas_relevantes(db: Session, informe: Informe, fechas: list):
    """Agrega o actualiza fechas relevantes asociadas a un informe."""
    for fecha in fechas:
        # Verificar si ya existe una combinación fecha/tipo/detalle
        existing_fecha = (
            db.query(FechaRelevante)
            .filter_by(
                expediente=informe.expediente,
                fecha=fecha["Fecha"],
                tipo=fecha["Tipo"],
                detalle=fecha["Detalle"],
            )
            .first()
        )
        if not existing_fecha:
            nueva_fecha = FechaRelevante(
                expediente=informe.expediente,
                fecha=fecha["Fecha"],
                tipo=fecha["Tipo"],
                detalle=fecha["Detalle"],
            )
            informe.fechas_relevantes.append(nueva_fecha)


def create_new_informe(informe: InformeClass) -> Informe:
    """Crea un nuevo informe con fechas relevantes."""
    nuevas_fechas = [
        FechaRelevante(
            expediente=informe.expediente,
            fecha=fecha["Fecha"],
            tipo=fecha["Tipo"],
            detalle=fecha["Detalle"],
        )
        for fecha in informe.fechas_relevantes
    ]
    return Informe(
        expediente=informe.expediente,
        jurisdiccion=informe.jurisdiccion,
        situacion_actual=informe.situacion_actual,
        dependencia=informe.dependencia,
        demandante=informe.demandante,
        demandado=informe.demandado,
        caratula=informe.caratula,
        tipo_demanda=informe.tipo_demanda,
        juzgado=informe.juzgado,
        fechas_relevantes=nuevas_fechas,
    )


def upsert(db: Session, informe: InformeClass):
    """
    Realiza un upsert del informe, insertando si no existe o actualizando si ya existe.
    :param db: sesión de la base de datos.
    :param informe: instancia de la clase Informe a insertar o actualizar.
    """
    try:
        existing_informe = find_existing_informe(db, informe.expediente)

        if existing_informe:
            logger.info(
                f"Informe con expediente {informe.expediente} encontrado. Actualizando..."
            )
            update_informe(existing_informe, informe)
            add_or_update_fechas_relevantes(
                db, existing_informe, informe.fechas_relevantes
            )
        else:
            logger.info(
                f"Informe con expediente {informe.expediente} no encontrado. Creando nuevo..."
            )
            nuevo_informe = create_new_informe(informe)
            db.add(nuevo_informe)

        db.commit()
        logger.info(
            f"Informe con expediente {informe.expediente} procesado exitosamente."
        )

    except IntegrityError as e:
        db.rollback()
        logger.error(
            f"Error de integridad al procesar el informe {informe.expediente}: {e}"
        )
    except Exception as e:
        db.rollback()
        logger.error(
            f"Error inesperado al procesar el informe {informe.expediente}: {e}"
        )


def upsert_execute(informe: InformeClass):
    """
    Ejecuta el método upsert utilizando una nueva sesión de base de datos.
    :param informe: instancia de la clase Informe a procesar.
    """
    db = SessionLocal()
    try:
        upsert(db, informe)
    finally:
        db.close()
