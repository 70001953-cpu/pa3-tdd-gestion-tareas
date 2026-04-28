################Sistema de Gestión de Tareas — TDD + ORM#####################################

**Universidad Continental | Construcción de Software | Unidad 3**

Proyecto desarrollado aplicando **Test-Driven Development (TDD)** con el ciclo
Red-Green-Refactor, **Katas TDD** y **SQLAlchemy ORM** para la persistencia de datos.

###################Integrantes###############################################################

| N° | Nombre |
|----|--------|
| 1  | Quispe Perez, Angelo Samir |

######################################## Descripción ########################################

Sistema CRUD de gestión de tareas con:
- Creación, listado, actualización y eliminación de tareas
- Prioridades (1-baja, 2-media, 3-alta)
- Estado completado / pendiente
- Estadísticas en tiempo real
- Persistencia con SQLAlchemy + SQLite

################################### Estructura del proyecto #################################

```
pa3-tdd-gestion-tareas/
├── src/
│   ├── __init__.py
│   ├── models.py              # Modelos ORM (SQLAlchemy)
│   └── servicio_tareas.py     # Lógica de negocio
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_servicio_tareas.py  # 30 pruebas unitarias TDD
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

######################################### Instalación ########################################

```bash
# 1. Clonar el repositorio
git clone https://github.com/70001953-cpu/pa3-tdd-gestion-tareas.git
cd pa3-tdd-gestion-tareas

# 2. Instalar dependencias
pip install -r requirements.txt
```

## 🧪 Ejecutar las pruebas

```bash
pytest tests/ -v
```

######################################## Resultado esperado ##################################

```
collected 30 items

tests/test_servicio_tareas.py::TestCrearTarea::test_crear_tarea_valida               PASSED
tests/test_servicio_tareas.py::TestCrearTarea::test_titulo_vacio_lanza_error          PASSED
tests/test_servicio_tareas.py::TestCrearTarea::test_prioridad_invalida_lanza_error    PASSED
tests/test_servicio_tareas.py::TestCrearTarea::test_prioridad_por_defecto_es_1        PASSED
tests/test_servicio_tareas.py::TestListarTareas::test_lista_vacia                     PASSED
tests/test_servicio_tareas.py::TestListarTareas::test_ordena_por_prioridad            PASSED
tests/test_servicio_tareas.py::TestCompletarTarea::test_cambia_estado                 PASSED
tests/test_servicio_tareas.py::TestEstadisticas::test_porcentaje_50                   PASSED
... (22 pruebas más)

===================== 30 passed in 0.82s ========================
```

####################################### Ciclo TDD aplicado ####################################

```
🔴 RED      → Escribir la prueba que falla (funcionalidad no existe aún)
🟢 GREEN    → Escribir el mínimo código para que la prueba pase
🔵 REFACTOR → Mejorar el código sin romper ninguna prueba
```

###################################### Katas desarrolladas ####################################

| Kata | Descripción            | Pruebas | Resultado   |
|------|------------------------|---------|-------------|
| 1    | Crear tarea            | 8       | ✅ 8/8 PASSED |
| 2    | Listar tareas          | 5       | ✅ 5/5 PASSED |
| 3    | Obtener tarea por ID   | 2       | ✅ 2/2 PASSED |
| 4    | Completar tarea        | 3       | ✅ 3/3 PASSED |
| 5    | Actualizar tarea       | 6       | ✅ 6/6 PASSED |
| 6    | Eliminar tarea         | 3       | ✅ 3/3 PASSED |
| 7    | Estadísticas           | 3       | ✅ 3/3 PASSED |
| **TOTAL** |                 | **30**  | ✅ **30/30** |

####################################### ORM — SQLAlchemy ######################################

```python
class Tarea(Base):
    __tablename__ = "tareas"
    id          = Column(Integer, primary_key=True)
    titulo      = Column(String(200), nullable=False)
    completada  = Column(Boolean, default=False)
    prioridad   = Column(Integer, default=1)   # 1=baja 2=media 3=alta
```

Las pruebas usan `sqlite:///:memory:` → cada test arranca con BD limpia.

########################################### Dependencias ######################################

```
pytest>=9.0.0
SQLAlchemy>=2.0.0
```

############################################# Repositorio #####################################

https://github.com/70001953-cpu/pa3-tdd-gestion-tareas


