# Pre-Entrega de Proyecto - Automatizaci�n QA

## ?? Descripci�n del Proyecto

Este proyecto contiene una suite de pruebas automatizadas para el sitio web **[SauceDemo](https://www.saucedemo.com)**, desarrollado como parte de la pre-entrega del curso de Automatizaci�n QA.

El objetivo es demostrar la capacidad para automatizar flujos b�sicos de navegaci�n web utilizando **Selenium WebDriver** y **Python**, aplicando los conocimientos adquiridos hasta la Clase 8 del curso.

### ? Funcionalidades Automatizadas

- **?? Login**: Autenticaci�n con credenciales v�lidas y validaci�n de acceso exitoso
- **?? Cat�logo**: Navegaci�n y verificaci�n de productos en el inventario
- **?? Carrito**: Interacci�n con el carrito de compras (agregar productos, verificar contador, validar items)

---

## ??? Tecnolog�as Utilizadas

| Tecnolog�a | Versi�n | Prop�sito |
|------------|---------|-----------|
| Python | 3.10+ | Lenguaje de programaci�n principal |
| Pytest | 8.3.5 | Framework de testing |
| Selenium WebDriver | 4.27.1 | Automatizaci�n de navegadores |
| WebDriver Manager | 4.0.2 | Gesti�n autom�tica de drivers |
| Pytest-HTML | 4.1.1 | Generaci�n de reportes HTML |
| Git/GitHub | - | Control de versiones |

---

## ?? Estructura del Proyecto

```
pre-entrega-proyecto/
�
+-- tests/                      # Casos de prueba automatizados
�   +-- __init__.py
�   +-- test_saucedemo.py       # Suite principal de tests
�
+-- utils/                      # Funciones auxiliares
�   +-- __init__.py
�   +-- helpers.py              # Helpers y selectores
�
+-- reports/                    # Reportes y capturas de pantalla
�   +-- (reportes generados)
�
+-- datos/                      # Datos externos (si aplica)
�
+-- conftest.py                 # Configuraci�n de Pytest y fixtures
+-- requirements.txt            # Dependencias del proyecto
+-- README.md                   # Este archivo
```

---

## ?? Instalaci�n y Configuraci�n

### Prerrequisitos

- Python 3.10 o superior instalado
- Google Chrome instalado
- Git instalado

### Pasos de Instalaci�n

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

## ?? Ejecuci�n de Pruebas

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

# Solo tests de cat�logo
pytest tests/test_saucedemo.py::TestCatalogo -v

# Solo tests de carrito
pytest tests/test_saucedemo.py::TestCarrito -v
```

### Ejecutar un test espec�fico
```bash
pytest tests/test_saucedemo.py::TestLogin::test_login_exitoso_con_credenciales_validas -v
```

---

## ?? Casos de Prueba Implementados

### 1. TestLogin (Automatizaci�n de Login)
| Test | Descripci�n | Criterio de Aceptaci�n |
|------|-------------|----------------------|
| test_login_exitoso_con_credenciales_validas | Login con usuario standard_user | Redirecci�n a /inventory.html y t�tulo "Products" |
| test_url_correcta_despues_de_login | Verificar URL post-login | URL exacta del inventario |

### 2. TestCatalogo (Navegaci�n y Verificaci�n)
| Test | Descripci�n | Criterio de Aceptaci�n |
|------|-------------|----------------------|
| test_titulo_pagina_inventario | Verificar t�tulo "Products" | T�tulo correcto visible |
| test_productos_visibles_en_inventario | Verificar existencia de productos | Al menos 1 producto presente |
| test_informacion_primer_producto | Obtener nombre/precio del primer producto | Datos v�lidos obtenidos |
| test_elementos_interfaz_presentes | Verificar men�, filtros, carrito | Todos los elementos presentes |

### 3. TestCarrito (Interacci�n con Productos)
| Test | Descripci�n | Criterio de Aceptaci�n |
|------|-------------|----------------------|
| test_agregar_producto_al_carrito | Agregar primer producto | Producto agregado exitosamente |
| test_contador_carrito_incrementa | Verificar badge del carrito | Contador muestra "1" |
| test_navegar_al_carrito | Navegar a p�gina del carrito | URL contiene /cart.html |
| test_producto_aparece_en_carrito | Verificar producto en carrito | Producto visible en lista |
| test_flujo_completo_agregar_y_verificar_carrito | Flujo E2E completo | Todos los pasos exitosos |

---

## ?? Reportes y Evidencias

### Reporte HTML
Despu�s de ejecutar las pruebas con la opci�n --html, el reporte se genera en la carpeta 
eports/.

### Capturas de Pantalla
En caso de fallo, se generan autom�ticamente capturas de pantalla en 
eports/ con el formato:
```
FALLO_{nombre_test}_{timestamp}.png
```

---

## ?? Credenciales de Prueba

Las credenciales utilizadas son las proporcionadas por SauceDemo para testing:

- **Usuario**: standard_user
- **Contrase�a**: secret_sauce

---

## 👤 Autor

- **Nombre**: Adolfo Enrique Brusquetti Cano
- **Email**: aebrusquetti@gmail.com
- **GitHub**: [adolfo-brusquetti-avenga](https://github.com/adolfo-brusquetti-avenga)

---

## ?? Notas Adicionales

- Los tests son independientes entre s� (la falla de uno no afecta a los dem�s)
- Se utilizan esperas expl�citas para mayor estabilidad
- El c�digo est� comentado y sigue buenas pr�cticas de programaci�n
- Compatible con Chrome (versi�n actual)

---

## ?? Historial de Cambios

| Fecha | Versi�n | Descripci�n |
|-------|---------|-------------|
| Mayo 2026 | 1.0.0 | Versi�n inicial - Pre-entrega |

---

**Curso de Automatizaci�n QA - Pre-Entrega de Proyecto**
