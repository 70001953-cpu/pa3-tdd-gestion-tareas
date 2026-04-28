"""
test_servicio_tareas.py
=======================
Suite completa de pruebas unitarias con enfoque TDD (Red-Green-Refactor).

Cada sección documenta el ciclo TDD seguido:
  🔴 RED    — Se escribe la prueba que falla porque la funcionalidad no existe aún.
  🟢 GREEN  — Se implementa el mínimo código necesario para que la prueba pase.
  🔵 REFACTOR — Se mejora el código sin cambiar su comportamiento.

Universidad Continental — Construcción de Software — Unidad 3
Autor: Angelo Samir Quispe Pérez
Herramientas: pytest, SQLAlchemy (SQLite en memoria)
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.models import Base, Tarea
from src.servicio_tareas import ServicioTareas


# ─────────────────────────────────────────────────────────────────────────────
# FIXTURE: Base de datos en memoria (aislada por cada prueba)
# ─────────────────────────────────────────────────────────────────────────────
@pytest.fixture
def servicio():
    """
    Crea un motor SQLite en memoria y una sesión limpia por cada test.
    Al usar ':memory:', cada prueba comienza con una BD completamente vacía,
    garantizando el aislamiento total (principio FIRST: Independent).
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    sesion = Session(engine)
    srv = ServicioTareas(sesion)
    yield srv
    sesion.close()
    Base.metadata.drop_all(engine)


# =============================================================================
# KATA 1 — CREAR TAREA
# Ciclo TDD:
#   🔴 RED: test_crear_tarea_valida falla (ServicioTareas no existe)
#   🟢 GREEN: se implementa crear_tarea() con validación básica
#   🔵 REFACTOR: se separa la validación en lógica propia
# =============================================================================

class TestCrearTarea:

    def test_crear_tarea_valida(self, servicio):
        """🟢 Crea una tarea con datos válidos y la persiste en la BD."""
        tarea = servicio.crear_tarea("Implementar login", "Módulo de autenticación", prioridad=3)

        assert tarea.id is not None
        assert tarea.titulo == "Implementar login"
        assert tarea.descripcion == "Módulo de autenticación"
        assert tarea.prioridad == 3
        assert tarea.completada is False

    def test_crear_tarea_titulo_vacio_lanza_error(self, servicio):
        """🔴→🟢 Título vacío debe lanzar ValueError (validación de negocio)."""
        with pytest.raises(ValueError, match="título"):
            servicio.crear_tarea("")

    def test_crear_tarea_titulo_solo_espacios_lanza_error(self, servicio):
        """🔴→🟢 Título con solo espacios también debe rechazarse."""
        with pytest.raises(ValueError, match="título"):
            servicio.crear_tarea("   ")

    def test_crear_tarea_prioridad_invalida_lanza_error(self, servicio):
        """🔴→🟢 Prioridad fuera de rango [1,2,3] debe lanzar ValueError."""
        with pytest.raises(ValueError, match="prioridad"):
            servicio.crear_tarea("Tarea X", prioridad=5)

    def test_crear_tarea_prioridad_cero_lanza_error(self, servicio):
        """🔴→🟢 Prioridad 0 no es válida."""
        with pytest.raises(ValueError, match="prioridad"):
            servicio.crear_tarea("Tarea X", prioridad=0)

    def test_crear_tarea_prioridad_por_defecto_es_1(self, servicio):
        """🟢 Sin especificar prioridad, el valor por defecto debe ser 1 (baja)."""
        tarea = servicio.crear_tarea("Sin prioridad explícita")
        assert tarea.prioridad == 1

    def test_crear_multiples_tareas_tienen_ids_distintos(self, servicio):
        """🟢 Cada tarea creada debe recibir un ID único autoincremental."""
        t1 = servicio.crear_tarea("Tarea A")
        t2 = servicio.crear_tarea("Tarea B")
        t3 = servicio.crear_tarea("Tarea C")
        assert len({t1.id, t2.id, t3.id}) == 3

    def test_crear_tarea_elimina_espacios_del_titulo(self, servicio):
        """🔵 REFACTOR: El servicio debe limpiar espacios del título."""
        tarea = servicio.crear_tarea("  Título con espacios  ")
        assert tarea.titulo == "Título con espacios"


# =============================================================================
# KATA 2 — LISTAR TAREAS
# =============================================================================

class TestListarTareas:

    def test_listar_devuelve_lista_vacia_si_no_hay_tareas(self, servicio):
        """🟢 BD vacía → listar_tareas() debe retornar lista vacía."""
        resultado = servicio.listar_tareas()
        assert resultado == []

    def test_listar_devuelve_todas_las_tareas(self, servicio):
        """🟢 Tres tareas creadas → listar devuelve exactamente tres."""
        servicio.crear_tarea("Tarea 1")
        servicio.crear_tarea("Tarea 2")
        servicio.crear_tarea("Tarea 3")
        assert len(servicio.listar_tareas()) == 3

    def test_listar_ordena_por_prioridad_descendente(self, servicio):
        """🔵 REFACTOR: Las tareas deben aparecer de mayor a menor prioridad."""
        servicio.crear_tarea("Baja",  prioridad=1)
        servicio.crear_tarea("Alta",  prioridad=3)
        servicio.crear_tarea("Media", prioridad=2)

        tareas = servicio.listar_tareas()
        prioridades = [t.prioridad for t in tareas]
        assert prioridades == sorted(prioridades, reverse=True)

    def test_listar_pendientes_solo_muestra_no_completadas(self, servicio):
        """🟢 listar_pendientes filtra correctamente."""
        t1 = servicio.crear_tarea("Pendiente")
        t2 = servicio.crear_tarea("Completada")
        servicio.completar_tarea(t2.id)

        pendientes = servicio.listar_pendientes()
        assert len(pendientes) == 1
        assert pendientes[0].id == t1.id

    def test_listar_completadas_solo_muestra_terminadas(self, servicio):
        """🟢 listar_completadas filtra correctamente."""
        t1 = servicio.crear_tarea("A completar")
        servicio.crear_tarea("No completada")
        servicio.completar_tarea(t1.id)

        completadas = servicio.listar_completadas()
        assert len(completadas) == 1
        assert completadas[0].completada is True


# =============================================================================
# KATA 3 — OBTENER TAREA POR ID
# =============================================================================

class TestObtenerTarea:

    def test_obtener_tarea_existente(self, servicio):
        """🟢 Obtener una tarea por ID válido devuelve el objeto correcto."""
        creada = servicio.crear_tarea("Mi tarea")
        obtenida = servicio.obtener_tarea(creada.id)
        assert obtenida.titulo == "Mi tarea"

    def test_obtener_tarea_inexistente_lanza_error(self, servicio):
        """🔴→🟢 ID que no existe debe lanzar ValueError."""
        with pytest.raises(ValueError, match="No existe"):
            servicio.obtener_tarea(999)


# =============================================================================
# KATA 4 — COMPLETAR TAREA
# =============================================================================

class TestCompletarTarea:

    def test_completar_tarea_cambia_estado(self, servicio):
        """🟢 Completar una tarea pendiente cambia completada a True."""
        tarea = servicio.crear_tarea("Tarea por completar")
        assert tarea.completada is False

        completada = servicio.completar_tarea(tarea.id)
        assert completada.completada is True

    def test_completar_tarea_ya_completada_lanza_error(self, servicio):
        """🔴→🟢 Completar una tarea que ya estaba completada lanza ValueError."""
        tarea = servicio.crear_tarea("Ya hecha")
        servicio.completar_tarea(tarea.id)

        with pytest.raises(ValueError, match="ya estaba completada"):
            servicio.completar_tarea(tarea.id)

    def test_completar_tarea_inexistente_lanza_error(self, servicio):
        """🔴→🟢 Completar una tarea que no existe lanza ValueError."""
        with pytest.raises(ValueError, match="No existe"):
            servicio.completar_tarea(404)


# =============================================================================
# KATA 5 — ACTUALIZAR TAREA
# =============================================================================

class TestActualizarTarea:

    def test_actualizar_titulo(self, servicio):
        """🟢 Actualizar solo el título deja los demás campos intactos."""
        tarea = servicio.crear_tarea("Título original", prioridad=2)
        actualizada = servicio.actualizar_tarea(tarea.id, titulo="Título nuevo")

        assert actualizada.titulo == "Título nuevo"
        assert actualizada.prioridad == 2   # sin cambios

    def test_actualizar_descripcion(self, servicio):
        """🟢 Actualizar solo la descripción."""
        tarea = servicio.crear_tarea("Tarea")
        actualizada = servicio.actualizar_tarea(tarea.id, descripcion="Nueva descripción")
        assert actualizada.descripcion == "Nueva descripción"

    def test_actualizar_prioridad(self, servicio):
        """🟢 Cambiar la prioridad de 1 a 3."""
        tarea = servicio.crear_tarea("Tarea baja", prioridad=1)
        actualizada = servicio.actualizar_tarea(tarea.id, prioridad=3)
        assert actualizada.prioridad == 3

    def test_actualizar_titulo_vacio_lanza_error(self, servicio):
        """🔴→🟢 No se puede actualizar el título a cadena vacía."""
        tarea = servicio.crear_tarea("Original")
        with pytest.raises(ValueError, match="vacío"):
            servicio.actualizar_tarea(tarea.id, titulo="")

    def test_actualizar_prioridad_invalida_lanza_error(self, servicio):
        """🔴→🟢 Prioridad inválida en actualización también lanza error."""
        tarea = servicio.crear_tarea("Tarea")
        with pytest.raises(ValueError, match="prioridad"):
            servicio.actualizar_tarea(tarea.id, prioridad=10)

    def test_actualizar_tarea_inexistente_lanza_error(self, servicio):
        """🔴→🟢 Actualizar ID inexistente lanza ValueError."""
        with pytest.raises(ValueError, match="No existe"):
            servicio.actualizar_tarea(999, titulo="Algo")


# =============================================================================
# KATA 6 — ELIMINAR TAREA
# =============================================================================

class TestEliminarTarea:

    def test_eliminar_tarea_existente(self, servicio):
        """🟢 Eliminar una tarea existente la quita de la BD."""
        tarea = servicio.crear_tarea("A eliminar")
        resultado = servicio.eliminar_tarea(tarea.id)

        assert resultado is True
        assert len(servicio.listar_tareas()) == 0

    def test_eliminar_reduce_el_total(self, servicio):
        """🟢 Después de eliminar, el conteo total disminuye."""
        t1 = servicio.crear_tarea("T1")
        servicio.crear_tarea("T2")
        servicio.crear_tarea("T3")

        servicio.eliminar_tarea(t1.id)
        assert len(servicio.listar_tareas()) == 2

    def test_eliminar_tarea_inexistente_lanza_error(self, servicio):
        """🔴→🟢 Eliminar ID que no existe lanza ValueError."""
        with pytest.raises(ValueError, match="No existe"):
            servicio.eliminar_tarea(777)


# =============================================================================
# KATA 7 — ESTADÍSTICAS
# =============================================================================

class TestEstadisticas:

    def test_estadisticas_bd_vacia(self, servicio):
        """🟢 Sin tareas, todas las estadísticas deben ser cero."""
        stats = servicio.estadisticas()
        assert stats["total"] == 0
        assert stats["completadas"] == 0
        assert stats["pendientes"] == 0
        assert stats["porcentaje_completado"] == 0.0

    def test_estadisticas_con_tareas_mixtas(self, servicio):
        """🟢 Con 4 tareas (2 completadas) → porcentaje = 50.0."""
        t1 = servicio.crear_tarea("T1")
        t2 = servicio.crear_tarea("T2")
        servicio.crear_tarea("T3")
        servicio.crear_tarea("T4")

        servicio.completar_tarea(t1.id)
        servicio.completar_tarea(t2.id)

        stats = servicio.estadisticas()
        assert stats["total"] == 4
        assert stats["completadas"] == 2
        assert stats["pendientes"] == 2
        assert stats["porcentaje_completado"] == 50.0

    def test_estadisticas_todas_completadas(self, servicio):
        """🟢 Con todas completadas → porcentaje = 100.0."""
        t1 = servicio.crear_tarea("T1")
        t2 = servicio.crear_tarea("T2")
        servicio.completar_tarea(t1.id)
        servicio.completar_tarea(t2.id)

        stats = servicio.estadisticas()
        assert stats["porcentaje_completado"] == 100.0
