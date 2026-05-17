# -*- coding: utf-8 -*-
"""
Test Suite para SauceDemo - Pre-Entrega Automatizacion QA
=========================================================
Casos de prueba automatizados para www.saucedemo.com

Autor: Adolfo Enrique Brusquetti Cano
Fecha: Mayo 2026
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import (
    realizar_login,
    verificar_login_exitoso,
    obtener_titulo_pagina,
    obtener_lista_productos,
    obtener_info_primer_producto,
    verificar_elementos_interfaz,
    agregar_primer_producto_al_carrito,
    obtener_contador_carrito,
    navegar_al_carrito,
    verificar_producto_en_carrito,
    obtener_items_carrito,
    capturar_pantalla,
    BASE_URL
)


# ==================== TEST CLASE 1: AUTOMATIZACION DE LOGIN ====================

class TestLogin:
    """Clase de pruebas para la funcionalidad de Login."""

    def test_login_exitoso_con_credenciales_validas(self, driver):
        """
        Caso de Prueba: Login con credenciales validas
        - Navegar a saucedemo.com
        - Ingresar credenciales (standard_user / secret_sauce)
        - Validar redireccion a /inventory.html
        """
        login_exitoso = realizar_login(driver)
        
        assert login_exitoso, "El login deberia ser exitoso con credenciales validas"
        assert "/inventory.html" in driver.current_url, \
            f"La URL deberia contener '/inventory.html', URL actual: {driver.current_url}"
        
        titulo = obtener_titulo_pagina(driver)
        assert titulo is not None, "El titulo de la pagina deberia estar presente"
        assert "Products" in titulo, f"El titulo deberia contener 'Products', titulo actual: {titulo}"
        
        print(f"Login exitoso - URL: {driver.current_url}")
        print(f"Titulo de pagina: {titulo}")


    def test_url_correcta_despues_de_login(self, driver):
        """Verifica URL correcta despues del login."""
        realizar_login(driver)
        
        url_actual = driver.current_url
        url_esperada = f"{BASE_URL}/inventory.html"
        
        assert url_actual == url_esperada, f"URL esperada: {url_esperada}, URL actual: {url_actual}"
        print(f"URL correcta despues del login: {url_actual}")


# ==================== TEST CLASE 2: NAVEGACION Y CATALOGO ====================

class TestCatalogo:
    """Clase de pruebas para navegacion y verificacion del catalogo."""

    def test_titulo_pagina_inventario(self, driver):
        """Verifica que el titulo de la pagina de inventario sea correcto."""
        realizar_login(driver)
        
        titulo = obtener_titulo_pagina(driver)
        
        assert titulo is not None, "El titulo deberia estar presente"
        assert titulo == "Products", f"El titulo deberia ser 'Products', titulo actual: {titulo}"
        print(f"Titulo de pagina verificado: {titulo}")


    def test_productos_visibles_en_inventario(self, driver):
        """Verifica que existan productos visibles en la pagina."""
        realizar_login(driver)
        
        productos = obtener_lista_productos(driver)
        
        assert len(productos) > 0, "Deberia haber al menos un producto visible en el inventario"
        print(f"Productos encontrados en inventario: {len(productos)}")


    def test_informacion_primer_producto(self, driver):
        """Obtiene y valida nombre y precio del primer producto."""
        realizar_login(driver)
        
        info_producto = obtener_info_primer_producto(driver)
        
        assert info_producto is not None, "Deberia poder obtener informacion del primer producto"
        assert "nombre" in info_producto, "Deberia contener el nombre del producto"
        assert "precio" in info_producto, "Deberia contener el precio del producto"
        assert len(info_producto["nombre"]) > 0, "El nombre no deberia estar vacio"
        
        print(f"Primer producto:")
        print(f"   Nombre: {info_producto['nombre']}")
        print(f"   Precio: {info_producto['precio']}")


    def test_elementos_interfaz_presentes(self, driver):
        """Valida que elementos importantes de la interfaz esten presentes."""
        realizar_login(driver)
        
        elementos = verificar_elementos_interfaz(driver)
        
        assert elementos["menu"], "El menu hamburguesa deberia estar presente"
        assert elementos["filtros"], "El dropdown de filtros deberia estar presente"
        assert elementos["carrito"], "El icono del carrito deberia estar presente"
        assert elementos["titulo"], "El titulo de la seccion deberia estar presente"
        
        print("Elementos de interfaz verificados:")
        for elemento, presente in elementos.items():
            estado = "OK" if presente else "FALTA"
            print(f"   {estado} - {elemento.capitalize()}")


# ==================== TEST CLASE 3: INTERACCION CON CARRITO ====================

class TestCarrito:
    """Clase de pruebas para interaccion con el carrito de compras."""

    def test_agregar_producto_al_carrito(self, driver):
        """Agrega el primer producto al carrito."""
        realizar_login(driver)
        
        nombre_producto = agregar_primer_producto_al_carrito(driver)
        
        assert nombre_producto is not None, "Deberia poder agregar un producto al carrito"
        print(f"Producto agregado al carrito: {nombre_producto}")


    def test_contador_carrito_incrementa(self, driver):
        """Verifica que el contador del carrito se incremente correctamente."""
        realizar_login(driver)
        
        contador_inicial = obtener_contador_carrito(driver)
        assert contador_inicial == 0, f"El contador inicial deberia ser 0, actual: {contador_inicial}"
        
        agregar_primer_producto_al_carrito(driver)
        
        contador_final = obtener_contador_carrito(driver)
        assert contador_final == 1, f"El contador deberia ser 1 despues de agregar un producto, actual: {contador_final}"
        
        print(f"Contador del carrito actualizado: {contador_inicial} -> {contador_final}")


    def test_navegar_al_carrito(self, driver):
        """Valida que se puede acceder a la pagina del carrito."""
        realizar_login(driver)
        agregar_primer_producto_al_carrito(driver)
        
        navegacion_exitosa = navegar_al_carrito(driver)
        
        assert navegacion_exitosa, "La navegacion al carrito deberia ser exitosa"
        assert "/cart.html" in driver.current_url, \
            f"La URL deberia contener '/cart.html', URL actual: {driver.current_url}"
        
        print(f"Navegacion al carrito exitosa - URL: {driver.current_url}")


    def test_producto_aparece_en_carrito(self, driver):
        """Verifica que el producto agregado aparezca correctamente en el carrito."""
        realizar_login(driver)
        
        nombre_producto = agregar_primer_producto_al_carrito(driver)
        navegar_al_carrito(driver)
        
        producto_en_carrito = verificar_producto_en_carrito(driver, nombre_producto)
        
        assert producto_en_carrito, f"El producto '{nombre_producto}' deberia estar en el carrito"
        
        items = obtener_items_carrito(driver)
        print(f"Producto verificado en carrito:")
        for item in items:
            print(f"   - {item['nombre']} | {item['precio']}")


    def test_flujo_completo_agregar_y_verificar_carrito(self, driver):
        """Flujo completo: Login -> Inventario -> Agregar -> Carrito -> Verificar"""
        # PASO 1: Login
        print("PASO 1: Realizando login...")
        login_exitoso = realizar_login(driver)
        assert login_exitoso, "Login deberia ser exitoso"
        print("   OK - Login exitoso")
        
        # PASO 2: Verificar inventario
        print("PASO 2: Verificando inventario...")
        productos = obtener_lista_productos(driver)
        assert len(productos) > 0, "Deberia haber productos en el inventario"
        print(f"   OK - {len(productos)} productos encontrados")
        
        # PASO 3: Agregar producto
        print("PASO 3: Agregando producto al carrito...")
        nombre_producto = agregar_primer_producto_al_carrito(driver)
        assert nombre_producto is not None, "Deberia poder agregar producto"
        print(f"   OK - Producto agregado: {nombre_producto}")
        
        # PASO 4: Verificar contador
        print("PASO 4: Verificando contador del carrito...")
        contador = obtener_contador_carrito(driver)
        assert contador == 1, f"Contador deberia ser 1, actual: {contador}"
        print(f"   OK - Contador correcto: {contador}")
        
        # PASO 5: Navegar al carrito
        print("PASO 5: Navegando al carrito...")
        navegar_al_carrito(driver)
        assert "/cart.html" in driver.current_url
        print("   OK - Navegacion exitosa")
        
        # PASO 6: Verificar producto en carrito
        print("PASO 6: Verificando producto en carrito...")
        producto_presente = verificar_producto_en_carrito(driver, nombre_producto)
        assert producto_presente, "Producto deberia estar en el carrito"
        print(f"   OK - Producto '{nombre_producto}' encontrado en carrito")
        
        print("\nFLUJO COMPLETO EXITOSO!")
