# Pre-Entrega de Proyecto - Automatizacion QA

## Descripcion del Proyecto

Este proyecto contiene una suite de pruebas automatizadas para el sitio web **[SauceDemo](https://www.saucedemo.com)**, desarrollado como parte de la pre-entrega del curso de Automatizacion QA.

El objetivo es demostrar la capacidad para automatizar flujos basicos de navegacion web utilizando **Selenium WebDriver** y **Python**, aplicando los conocimientos adquiridos hasta la Clase 8 del curso.

### Funcionalidades Automatizadas

- **Login**: Autenticacion con credenciales validas y validacion de acceso exitoso
- **Catalogo**: Navegacion y verificacion de productos en el inventario
- **Carrito**: Interaccion con el carrito de compras (agregar productos, verificar contador, validar items)

---

## Tecnologias Utilizadas

| Tecnologia | Version | Proposito |
|------------|---------|-----------|
| Python | 3.10+ | Lenguaje de programacion principal |
| Pytest | 8.3.5 | Framework de testing |
| Selenium WebDriver | 4.27.1 | Automatizacion de navegadores |
| WebDriver Manager | 4.0.2 | Gestion automatica de drivers |
| Pytest-HTML | 4.1.1 | Generacion de reportes HTML |
| Git/GitHub | - | Control de versiones |

---

## Estructura del Proyecto

```
pre-entrega-proyecto/
|
|-- tests/                      # Casos de prueba automatizados
|   |-- __init__.py
|   |-- test_saucedemo.py       # Suite principal de tests
|
|-- utils/                      # Funciones auxiliares
|   |-- __init__.py
|   |-- helpers.py              # Helpers y selectores
|
|-- reports/                    # Reportes y capturas de pantalla
|   |-- (reportes generados)
|
|-- datos/                      # Datos externos (si aplica)
|
|-- conftest.py                 # Configuracion de Pytest y fixtures
|-- requirements.txt            # Dependencias del proyecto
|-- README.md                   # Este archivo
```

---

## Instalacion y Configuracion

### Prerrequisitos

- Python 3.10 o superior instalado
- Google Chrome instalado
- Git instalado

### Pasos de Instalacion

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/pre-entrega-automation-testing-nombre-apellido.git
cd pre-entrega-automation-testing-nombre-apellido
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

---

## Ejecucion de Pruebas

### Ejecutar todas las pruebas
```bash
pytest tests/test_saucedemo.py -v
```

### Ejecutar con reporte HTML
```bash
pytest tests/test_saucedemo.py -v --html=reports/reporte.html
```

### Ejecutar por clase de test
```bash
# Solo tests de login
pytest tests/test_saucedemo.py::TestLogin -v

# Solo tests de catalogo
pytest tests/test_saucedemo.py::TestCatalogo -v

# Solo tests de carrito
pytest tests/test_saucedemo.py::TestCarrito -v
```

### Ejecutar un test especifico
```bash
pytest tests/test_saucedemo.py::TestLogin::test_login_exitoso_con_credenciales_validas -v
```

---

## Casos de Prueba Implementados

### 1. TestLogin (Automatizacion de Login)
| Test | Descripcion | Criterio de Aceptacion |
|------|-------------|----------------------|
| test_login_exitoso_con_credenciales_validas | Login con usuario standard_user | Redireccion a /inventory.html y titulo "Products" |
| test_url_correcta_despues_de_login | Verificar URL post-login | URL exacta del inventario |

### 2. TestCatalogo (Navegacion y Verificacion)
| Test | Descripcion | Criterio de Aceptacion |
|------|-------------|----------------------|
| test_titulo_pagina_inventario | Verificar titulo "Products" | Titulo correcto visible |
| test_productos_visibles_en_inventario | Verificar existencia de productos | Al menos 1 producto presente |
| test_informacion_primer_producto | Obtener nombre/precio del primer producto | Datos validos obtenidos |
| test_elementos_interfaz_presentes | Verificar menu, filtros, carrito | Todos los elementos presentes |

### 3. TestCarrito (Interaccion con Productos)
| Test | Descripcion | Criterio de Aceptacion |
|------|-------------|----------------------|
| test_agregar_producto_al_carrito | Agregar primer producto | Producto agregado exitosamente |
| test_contador_carrito_incrementa | Verificar badge del carrito | Contador muestra "1" |
| test_navegar_al_carrito | Navegar a pagina del carrito | URL contiene /cart.html |
| test_producto_aparece_en_carrito | Verificar producto en carrito | Producto visible en lista |
| test_flujo_completo_agregar_y_verificar_carrito | Flujo E2E completo | Todos los pasos exitosos |

---

## Reportes y Evidencias

### Reporte HTML
Despues de ejecutar las pruebas con la opcion `--html`, el reporte se genera en la carpeta `reports/`.

### Capturas de Pantalla
En caso de fallo, se generan automaticamente capturas de pantalla en `reports/` con el formato:
```
FALLO_{nombre_test}_{timestamp}.png
```

---

## Credenciales de Prueba

Las credenciales utilizadas son las proporcionadas por SauceDemo para testing:

- **Usuario**: standard_user
- **Contrasena**: secret_sauce

---

## Documentacion Detallada del Codigo

A continuacion se describe en detalle cada archivo del proyecto y sus funciones principales.

---

### Archivo: `conftest.py`

Este archivo contiene la configuracion global de Pytest, incluyendo fixtures y hooks.

#### Fixture: `driver()`
```python
@pytest.fixture(scope="function")
def driver():
```
- **Proposito**: Proporciona una instancia del navegador Chrome para cada test.
- **Scope**: `function` - Se crea una nueva instancia para cada funcion de test.
- **Configuracion aplicada**:
  - `--start-maximized`: Abre el navegador en pantalla completa.
  - `--disable-extensions`: Desactiva extensiones para evitar interferencias.
  - `--disable-popup-blocking`: Evita que se bloqueen ventanas emergentes.
  - `--disable-infobars`: Oculta barras de informacion del navegador.
  - `implicitly_wait(10)`: Espera implicita de 10 segundos para encontrar elementos.
- **Limpieza**: Al finalizar cada test, ejecuta `driver.quit()` para cerrar el navegador.

#### Hook: `pytest_runtest_makereport()`
```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
```
- **Proposito**: Captura automaticamente una screenshot cuando un test falla.
- **Funcionamiento**:
  1. Intercepta el resultado de cada test despues de su ejecucion (`report.when == "call"`).
  2. Si el test fallo (`report.failed`), obtiene la instancia del driver.
  3. Crea la carpeta `reports/` si no existe.
  4. Guarda una imagen PNG con formato: `FALLO_{nombre_test}_{timestamp}.png`.

#### Funcion: `pytest_configure()`
```python
def pytest_configure(config):
```
- **Proposito**: Registra marcadores personalizados para categorizar tests.
- **Marcadores registrados**: `login`, `catalogo`, `carrito`.

#### Funcion: `pytest_html_report_title()`
```python
def pytest_html_report_title(report):
```
- **Proposito**: Personaliza el titulo del reporte HTML generado por pytest-html.

---

### Archivo: `utils/helpers.py`

Modulo con funciones auxiliares para interactuar con SauceDemo.

#### Constantes
| Constante | Valor | Descripcion |
|-----------|-------|-------------|
| `BASE_URL` | `https://www.saucedemo.com` | URL base del sitio de pruebas |
| `TIMEOUT_DEFAULT` | `10` | Tiempo maximo de espera en segundos |
| `CREDENCIALES_VALIDAS` | `{usuario, password}` | Credenciales de prueba |

#### Diccionarios de Selectores
- **`SELECTORES_LOGIN`**: Selectores para la pagina de inicio de sesion (campos de usuario, password, boton login, mensaje de error).
- **`SELECTORES_INVENTARIO`**: Selectores para la pagina de productos (titulo, lista de productos, precios, botones agregar, menu, filtros, carrito).
- **`SELECTORES_CARRITO`**: Selectores para la pagina del carrito (items, nombres, precios, botones).

#### Funciones de Navegacion

| Funcion | Parametros | Retorno | Descripcion |
|---------|------------|---------|-------------|
| `navegar_a_pagina()` | `driver`, `url` | Ninguno | Navega el navegador a la URL especificada |
| `esperar_elemento()` | `driver`, `locator`, `timeout` | Elemento o `None` | Espera hasta que un elemento sea visible en la pagina |
| `esperar_elemento_clickeable()` | `driver`, `locator`, `timeout` | Elemento o `None` | Espera hasta que un elemento pueda ser clickeado |

#### Funciones de Login

| Funcion | Parametros | Retorno | Descripcion |
|---------|------------|---------|-------------|
| `realizar_login()` | `driver`, `usuario`, `password` | `bool` | Ejecuta el flujo completo de login: navega a la pagina, ingresa credenciales y hace click en el boton. Retorna `True` si el login fue exitoso |
| `verificar_login_exitoso()` | `driver`, `timeout` | `bool` | Verifica que la URL contenga `/inventory.html` y que el titulo "Products" este visible |

#### Funciones de Inventario

| Funcion | Parametros | Retorno | Descripcion |
|---------|------------|---------|-------------|
| `obtener_titulo_pagina()` | `driver` | `str` o `None` | Obtiene el texto del titulo de la pagina (ej: "Products") |
| `obtener_lista_productos()` | `driver` | `list` | Retorna una lista con todos los elementos de producto del inventario |
| `obtener_info_primer_producto()` | `driver` | `dict` o `None` | Retorna un diccionario con `nombre` y `precio` del primer producto |
| `verificar_elementos_interfaz()` | `driver` | `dict` | Retorna un diccionario indicando si cada elemento de la interfaz esta presente (`menu`, `filtros`, `carrito`, `titulo`) |

#### Funciones de Carrito

| Funcion | Parametros | Retorno | Descripcion |
|---------|------------|---------|-------------|
| `agregar_primer_producto_al_carrito()` | `driver` | `str` o `None` | Hace click en el boton "Add to cart" del primer producto. Retorna el nombre del producto agregado |
| `obtener_contador_carrito()` | `driver` | `int` | Retorna el numero que muestra el badge del carrito (0 si no hay badge visible) |
| `navegar_al_carrito()` | `driver` | `bool` | Hace click en el icono del carrito y espera la navegacion a `/cart.html` |
| `verificar_producto_en_carrito()` | `driver`, `nombre_producto` | `bool` | Busca si un producto especifico esta en la lista del carrito |
| `obtener_items_carrito()` | `driver` | `list` | Retorna una lista de diccionarios con `nombre` y `precio` de cada item en el carrito |
| `capturar_pantalla()` | `driver`, `nombre_archivo`, `carpeta` | `str` | Guarda una screenshot con timestamp y retorna la ruta del archivo |

---

### Archivo: `tests/test_saucedemo.py`

Suite principal de pruebas automatizadas organizada en tres clases.

#### Clase: `TestLogin`
Pruebas para validar la funcionalidad de inicio de sesion.

| Metodo | Descripcion | Validaciones |
|--------|-------------|--------------|
| `test_login_exitoso_con_credenciales_validas()` | Verifica que el login funcione con credenciales correctas | URL contiene `/inventory.html`, titulo es "Products" |
| `test_url_correcta_despues_de_login()` | Verifica que la URL sea exactamente la esperada | URL es `https://www.saucedemo.com/inventory.html` |

#### Clase: `TestCatalogo`
Pruebas para validar la navegacion y visualizacion del catalogo de productos.

| Metodo | Descripcion | Validaciones |
|--------|-------------|--------------|
| `test_titulo_pagina_inventario()` | Verifica el titulo de la pagina | Titulo es exactamente "Products" |
| `test_productos_visibles_en_inventario()` | Verifica que existan productos | Lista de productos tiene al menos 1 elemento |
| `test_informacion_primer_producto()` | Obtiene datos del primer producto | El diccionario contiene `nombre` y `precio` no vacios |
| `test_elementos_interfaz_presentes()` | Verifica elementos de la UI | Menu, filtros, carrito y titulo estan presentes |

#### Clase: `TestCarrito`
Pruebas para validar la interaccion con el carrito de compras.

| Metodo | Descripcion | Validaciones |
|--------|-------------|--------------|
| `test_agregar_producto_al_carrito()` | Agrega un producto al carrito | Funcion retorna el nombre del producto |
| `test_contador_carrito_incrementa()` | Verifica que el badge se actualice | Contador pasa de 0 a 1 |
| `test_navegar_al_carrito()` | Navega a la pagina del carrito | URL contiene `/cart.html` |
| `test_producto_aparece_en_carrito()` | Verifica producto en el carrito | El producto agregado esta en la lista |
| `test_flujo_completo_agregar_y_verificar_carrito()` | Flujo E2E de 6 pasos | Login -> Inventario -> Agregar -> Contador -> Navegar -> Verificar |

---

## Autor

- **Nombre**: Adolfo Enrique Brusquetti Cano
- **Email**: aebrusquetti@gmail.com
- **GitHub**: [adolfo-brusquetti-avenga](https://github.com/adolfo-brusquetti-avenga)

---

## Notas Adicionales

- Los tests son independientes entre si (la falla de uno no afecta a los demas)
- Se utilizan esperas explicitas para mayor estabilidad
- El codigo esta comentado y sigue buenas practicas de programacion
- Compatible con Chrome (version actual)

---

## Historial de Cambios

| Fecha | Version | Descripcion |
|-------|---------|-------------|
| Mayo 2026 | 1.0.0 | Version inicial - Pre-entrega |

---

**Curso de Automatizacion QA - Pre-Entrega de Proyecto**
