from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class Informe(Base):
    """
    Clase que representa un informe para SQLAlchemy.
    """

    __tablename__ = "informes"
    __table_args__ = (UniqueConstraint("expediente", name="uq_expediente"),)

    expediente = Column(String(50), nullable=False, primary_key=True, unique=True)
    situacion_actual = Column(String(255))
    jurisdiccion = Column(String(255))
    dependencia = Column(String(255))
    demandante = Column(String(255))
    demandado = Column(String(255))
    caratula = Column(String(255))
    tipo_demanda = Column(String(255))
    juzgado = Column(String(255))

    fechas_relevantes = relationship(
        "FechaRelevante", back_populates="informe", cascade="all, delete-orphan"
    )


class FechaRelevante(Base):
    """
    Fechas relevantes asociadas a un informe.
    """

    __tablename__ = "fechas_relevantes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    expediente = Column(String(50), ForeignKey("informes.expediente"), nullable=False)
    fecha = Column(String(10), nullable=False)
    tipo = Column(String(255), nullable=False)
    detalle = Column(String(255), nullable=False)

    informe = relationship("Informe", back_populates="fechas_relevantes")
    __table_args__ = (
        UniqueConstraint(
            "expediente", "fecha", "tipo", "detalle", name="uq_fecha_detalle"
        ),
    )
