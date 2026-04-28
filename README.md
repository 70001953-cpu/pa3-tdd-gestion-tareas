# Sistema de Gestión de Tareas — TDD + ORM

**Universidad Continental | Construcción de Software | Unidad 3**

Proyecto desarrollado aplicando **Test-Driven Development (TDD)** con el ciclo
Red-Green-Refactor, **Katas TDD** y **SQLAlchemy ORM** para la persistencia de datos.

## 👥 Integrantes

| N° | Nombre |
|----|--------|
| 1 | Angelo Samir Quispe Pérez |

## 📋 Descripción

Sistema CRUD de gestión de tareas con:
- Creación, listado, actualización y eliminación de tareas
- Prioridades (1-baja, 2-media, 3-alta)
- Estado completado/pendiente
- Estadísticas en tiempo real
- Persistencia con SQLAlchemy + SQLite

## 🗂️ Estructura del proyecto

```
proyecto_tdd/
├── src/
│   ├── __init__.py
│   ├── models.py              # Modelos ORM (SQLAlchemy)
│   └── servicio_tareas.py     # Lógica de negocio (servicio)
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_servicio_tareas.py  # 30 pruebas unitarias TDD
├── requirements.txt
├── pytest.ini
└── README.md
```

## ⚙️ Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/proyecto-tdd-tareas.git
cd proyecto-tdd-tareas

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt
```

## 🧪 Ejecutar pruebas

```bash
# Todas las pruebas con detalle
pytest tests/ -v

# Con reporte de cobertura
pytest tests/ -v --cov=src --cov-report=term-missing
```

### Resultado esperado

```
collected 30 items
PASSED TestCrearTarea::test_crear_tarea_valida
PASSED TestCrearTarea::test_crear_tarea_titulo_vacio_lanza_error
... (27 pruebas más)
30 passed in 0.82s
```

## 🔄 Ciclo TDD aplicado

```
🔴 RED    → Escribir la prueba que falla
🟢 GREEN  → Implementar el mínimo código para que pase
🔵 REFACTOR → Mejorar el código sin romper las pruebas
```

### Katas desarrolladas

| Kata | Descripción | Pruebas |
|------|-------------|---------|
| 1    | Crear tarea | 8 pruebas |
| 2    | Listar tareas | 5 pruebas |
| 3    | Obtener tarea por ID | 2 pruebas |
| 4    | Completar tarea | 3 pruebas |
| 5    | Actualizar tarea | 6 pruebas |
| 6    | Eliminar tarea | 3 pruebas |
| 7    | Estadísticas | 3 pruebas |

## 🗄️ ORM — SQLAlchemy

Se usa **SQLAlchemy 2.x** con patrón **Session + DeclarativeBase**:

```python
class Tarea(Base):
    __tablename__ = "tareas"
    id          = Column(Integer, primary_key=True)
    titulo      = Column(String(200), nullable=False)
    completada  = Column(Boolean, default=False)
    prioridad   = Column(Integer, default=1)
```

Las pruebas usan `sqlite:///:memory:` para aislamiento total.

## 📦 Dependencias

```
pytest==9.0.3
SQLAlchemy==2.x
pytest-cov (opcional, para cobertura)
```

## 📄 Licencia

MIT — Universidad Continental 2025
