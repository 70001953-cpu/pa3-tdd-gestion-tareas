"""
servicio_tareas.py
==================
Capa de servicio con la lógica de negocio del sistema de gestión de tareas.
Aplica principios de responsabilidad única y facilita las pruebas unitarias.

Universidad Continental — Construcción de Software — Unidad 3
Autor: Angelo Samir Quispe Pérez
"""

from sqlalchemy.orm import Session
from .models import Tarea


class ServicioTareas:
    """
    Clase de servicio que encapsula las operaciones sobre Tarea.
    Recibe una sesión de SQLAlchemy por inyección de dependencias,
    lo que permite usar una BD en memoria durante las pruebas (TDD).
    """

    def __init__(self, sesion: Session) -> None:
        self.sesion = sesion

    # ── Crear ────────────────────────────────────────────────────────────────
    def crear_tarea(self, titulo: str, descripcion: str = "", prioridad: int = 1) -> Tarea:
        """
        Crea y persiste una nueva tarea.

        Raises:
            ValueError: Si el título está vacío o la prioridad no está entre 1 y 3.
        """
        if not titulo or not titulo.strip():
            raise ValueError("El título de la tarea no puede estar vacío.")
        if prioridad not in (1, 2, 3):
            raise ValueError("La prioridad debe ser 1 (baja), 2 (media) o 3 (alta).")

        tarea = Tarea(titulo=titulo.strip(), descripcion=descripcion, prioridad=prioridad)
        self.sesion.add(tarea)
        self.sesion.commit()
        self.sesion.refresh(tarea)
        return tarea

    # ── Listar ───────────────────────────────────────────────────────────────
    def listar_tareas(self) -> list[Tarea]:
        """Devuelve todas las tareas ordenadas por prioridad descendente."""
        return (
            self.sesion.query(Tarea)
            .order_by(Tarea.prioridad.desc(), Tarea.id.asc())
            .all()
        )

    def listar_pendientes(self) -> list[Tarea]:
        """Devuelve solo las tareas no completadas."""
        return self.sesion.query(Tarea).filter(Tarea.completada == False).all()

    def listar_completadas(self) -> list[Tarea]:
        """Devuelve solo las tareas completadas."""
        return self.sesion.query(Tarea).filter(Tarea.completada == True).all()

    # ── Obtener ──────────────────────────────────────────────────────────────
    def obtener_tarea(self, tarea_id: int) -> Tarea:
        """
        Busca una tarea por su ID.

        Raises:
            ValueError: Si la tarea no existe.
        """
        tarea = self.sesion.get(Tarea, tarea_id)
        if tarea is None:
            raise ValueError(f"No existe una tarea con id={tarea_id}.")
        return tarea

    # ── Completar ─────────────────────────────────────────────────────────────
    def completar_tarea(self, tarea_id: int) -> Tarea:
        """
        Marca una tarea como completada.

        Raises:
            ValueError: Si la tarea no existe o ya está completada.
        """
        tarea = self.obtener_tarea(tarea_id)
        if tarea.completada:
            raise ValueError(f"La tarea id={tarea_id} ya estaba completada.")
        tarea.completada = True
        self.sesion.commit()
        self.sesion.refresh(tarea)
        return tarea

    # ── Actualizar ────────────────────────────────────────────────────────────
    def actualizar_tarea(
        self,
        tarea_id: int,
        titulo: str | None = None,
        descripcion: str | None = None,
        prioridad: int | None = None,
    ) -> Tarea:
        """
        Actualiza uno o más campos de una tarea existente.

        Raises:
            ValueError: Si la tarea no existe, el título es vacío
                        o la prioridad es inválida.
        """
        tarea = self.obtener_tarea(tarea_id)

        if titulo is not None:
            if not titulo.strip():
                raise ValueError("El título no puede estar vacío.")
            tarea.titulo = titulo.strip()

        if descripcion is not None:
            tarea.descripcion = descripcion

        if prioridad is not None:
            if prioridad not in (1, 2, 3):
                raise ValueError("La prioridad debe ser 1, 2 o 3.")
            tarea.prioridad = prioridad

        self.sesion.commit()
        self.sesion.refresh(tarea)
        return tarea

    # ── Eliminar ──────────────────────────────────────────────────────────────
    def eliminar_tarea(self, tarea_id: int) -> bool:
        """
        Elimina una tarea por su ID.

        Returns:
            True si se eliminó correctamente.

        Raises:
            ValueError: Si la tarea no existe.
        """
        tarea = self.obtener_tarea(tarea_id)
        self.sesion.delete(tarea)
        self.sesion.commit()
        return True

    # ── Estadísticas ──────────────────────────────────────────────────────────
    def estadisticas(self) -> dict:
        """Devuelve un resumen estadístico de las tareas."""
        total       = self.sesion.query(Tarea).count()
        completadas = self.sesion.query(Tarea).filter(Tarea.completada == True).count()
        pendientes  = total - completadas
        return {
            "total":       total,
            "completadas": completadas,
            "pendientes":  pendientes,
            "porcentaje_completado": round((completadas / total * 100), 1) if total > 0 else 0.0,
        }
