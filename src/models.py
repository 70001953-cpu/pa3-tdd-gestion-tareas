"""
models.py
=========
Modelos ORM con SQLAlchemy para el sistema de gestión de tareas.
Universidad Continental — Construcción de Software — Unidad 3
Autor: Angelo Samir Quispe Pérez
"""

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Session
from datetime import datetime


# ─── Base declarativa (SQLAlchemy 2.x) ───────────────────────────────────────
class Base(DeclarativeBase):
    pass


# ─── Modelo: Tarea ────────────────────────────────────────────────────────────
class Tarea(Base):
    """Representa una tarea dentro del sistema de gestión."""

    __tablename__ = "tareas"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    titulo      = Column(String(200), nullable=False)
    descripcion = Column(String(500), nullable=True)
    completada  = Column(Boolean, default=False, nullable=False)
    prioridad   = Column(Integer, default=1, nullable=False)   # 1=baja, 2=media, 3=alta
    creada_en   = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        estado = "✓" if self.completada else "○"
        return f"<Tarea [{estado}] id={self.id} titulo='{self.titulo}' prioridad={self.prioridad}>"


# ─── Fábrica de motor / sesión ────────────────────────────────────────────────
def crear_engine(url: str = "sqlite:///tareas.db"):
    """Crea el motor de base de datos y genera las tablas si no existen."""
    engine = create_engine(url, echo=False)
    Base.metadata.create_all(engine)
    return engine


def obtener_sesion(engine) -> Session:
    """Devuelve una sesión de SQLAlchemy ligada al motor recibido."""
    return Session(engine)
