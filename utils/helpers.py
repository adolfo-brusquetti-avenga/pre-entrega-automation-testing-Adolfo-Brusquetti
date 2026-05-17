# -*- coding: utf-8 -*-
"""
Modulo de funciones auxiliares para automatizacion de SauceDemo
================================================================
Este modulo contiene funciones helper para interactuar con el sitio
www.saucedemo.com durante las pruebas automatizadas.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from datetime import datetime


# ==================== CONSTANTES ====================
BASE_URL = "https://www.saucedemo.com"
TIMEOUT_DEFAULT = 10

# Credenciales de prueba validas
CREDENCIALES_VALIDAS = {
    "usuario": "standard_user",
    "password": "secret_sauce"
}

# Selectores de elementos - Pagina de Login
SELECTORES_LOGIN = {
    "input_usuario": (By.ID, "user-name"),
    "input_password": (By.ID, "password"),
    "boton_login": (By.ID, "login-button"),
    "mensaje_error": (By.CSS_SELECTOR, "[data-test='error']")
}

# Selectores de elementos - Pagina de Inventario
SELECTORES_INVENTARIO = {
    "titulo_productos": (By.CLASS_NAME, "title"),
    "lista_productos": (By.CLASS_NAME, "inventory_item"),
    "nombre_producto": (By.CLASS_NAME, "inventory_item_name"),
    "precio_producto": (By.CLASS_NAME, "inventory_item_price"),
    "boton_agregar": (By.CSS_SELECTOR, "button[data-test^='add-to-cart']"),
    "menu_hamburguesa": (By.ID, "react-burger-menu-btn"),
    "filtro_dropdown": (By.CLASS_NAME, "product_sort_container"),
    "carrito_icono": (By.CLASS_NAME, "shopping_cart_link"),
    "carrito_contador": (By.CLASS_NAME, "shopping_cart_badge")
}

# Selectores de elementos - Pagina del Carrito
SELECTORES_CARRITO = {
    "items_carrito": (By.CLASS_NAME, "cart_item"),
    "nombre_item": (By.CLASS_NAME, "inventory_item_name"),
    "precio_item": (By.CLASS_NAME, "inventory_item_price"),
    "boton_checkout": (By.ID, "checkout"),
    "boton_continuar_comprando": (By.ID, "continue-shopping"),
    "boton_remover": (By.CSS_SELECTOR, "button[data-test^='remove']")
}


# ==================== FUNCIONES DE NAVEGACION ====================

def navegar_a_pagina(driver, url=BASE_URL):
    """Navega a la URL especificada."""
    driver.get(url)


def esperar_elemento(driver, locator, timeout=TIMEOUT_DEFAULT):
    """Espera explicita hasta que un elemento este presente y visible."""
    try:
        elemento = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return elemento
    except TimeoutException:
        return None


def esperar_elemento_clickeable(driver, locator, timeout=TIMEOUT_DEFAULT):
    """Espera explicita hasta que un elemento sea clickeable."""
    try:
        elemento = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        return elemento
    except TimeoutException:
        return None


# ==================== FUNCIONES DE LOGIN ====================

def realizar_login(driver, usuario=None, password=None):
    """Realiza el proceso de login en SauceDemo."""
    if usuario is None:
        usuario = CREDENCIALES_VALIDAS["usuario"]
    if password is None:
        password = CREDENCIALES_VALIDAS["password"]
    
    navegar_a_pagina(driver)
    
    input_usuario = esperar_elemento(driver, SELECTORES_LOGIN["input_usuario"])
    if input_usuario:
        input_usuario.clear()
        input_usuario.send_keys(usuario)
    
    input_password = esperar_elemento(driver, SELECTORES_LOGIN["input_password"])
    if input_password:
        input_password.clear()
        input_password.send_keys(password)
    
    boton_login = esperar_elemento_clickeable(driver, SELECTORES_LOGIN["boton_login"])
    if boton_login:
        boton_login.click()
    
    return verificar_login_exitoso(driver)


def verificar_login_exitoso(driver, timeout=TIMEOUT_DEFAULT):
    """Verifica si el login fue exitoso."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.url_contains("/inventory.html")
        )
        titulo = esperar_elemento(driver, SELECTORES_INVENTARIO["titulo_productos"])
        return titulo is not None and "Products" in titulo.text
    except TimeoutException:
        return False


# ==================== FUNCIONES DE INVENTARIO ====================

def obtener_titulo_pagina(driver):
    """Obtiene el titulo de la pagina de inventario."""
    titulo = esperar_elemento(driver, SELECTORES_INVENTARIO["titulo_productos"])
    return titulo.text if titulo else None


def obtener_lista_productos(driver):
    """Obtiene la lista de todos los productos en el inventario."""
    productos = driver.find_elements(*SELECTORES_INVENTARIO["lista_productos"])
    return productos


def obtener_info_primer_producto(driver):
    """Obtiene nombre y precio del primer producto del inventario."""
    nombres = driver.find_elements(*SELECTORES_INVENTARIO["nombre_producto"])
    precios = driver.find_elements(*SELECTORES_INVENTARIO["precio_producto"])
    
    if nombres and precios:
        return {
            "nombre": nombres[0].text,
            "precio": precios[0].text
        }
    return None


def verificar_elementos_interfaz(driver):
    """Verifica que los elementos importantes de la interfaz esten presentes."""
    elementos = {
        "menu": esperar_elemento(driver, SELECTORES_INVENTARIO["menu_hamburguesa"]) is not None,
        "filtros": esperar_elemento(driver, SELECTORES_INVENTARIO["filtro_dropdown"]) is not None,
        "carrito": esperar_elemento(driver, SELECTORES_INVENTARIO["carrito_icono"]) is not None,
        "titulo": esperar_elemento(driver, SELECTORES_INVENTARIO["titulo_productos"]) is not None
    }
    return elementos


# ==================== FUNCIONES DE CARRITO ====================

def agregar_primer_producto_al_carrito(driver):
    """Agrega el primer producto disponible al carrito."""
    info_producto = obtener_info_primer_producto(driver)
    
    botones_agregar = driver.find_elements(*SELECTORES_INVENTARIO["boton_agregar"])
    if botones_agregar:
        botones_agregar[0].click()
        return info_producto["nombre"] if info_producto else "Producto desconocido"
    return None


def obtener_contador_carrito(driver):
    """Obtiene el numero que muestra el contador del carrito."""
    try:
        badge = driver.find_element(*SELECTORES_INVENTARIO["carrito_contador"])
        return int(badge.text)
    except:
        return 0


def navegar_al_carrito(driver):
    """Navega a la pagina del carrito de compras."""
    icono_carrito = esperar_elemento_clickeable(driver, SELECTORES_INVENTARIO["carrito_icono"])
    if icono_carrito:
        icono_carrito.click()
        try:
            WebDriverWait(driver, TIMEOUT_DEFAULT).until(
                EC.url_contains("/cart.html")
            )
            return True
        except TimeoutException:
            return False
    return False


def verificar_producto_en_carrito(driver, nombre_producto):
    """Verifica que un producto especifico este en el carrito."""
    items = driver.find_elements(*SELECTORES_CARRITO["items_carrito"])
    for item in items:
        nombre = item.find_element(*SELECTORES_CARRITO["nombre_item"])
        if nombre_producto in nombre.text:
            return True
    return False


def obtener_items_carrito(driver):
    """Obtiene la lista de items en el carrito."""
    items = driver.find_elements(*SELECTORES_CARRITO["items_carrito"])
    lista_items = []
    
    for item in items:
        nombre = item.find_element(*SELECTORES_CARRITO["nombre_item"]).text
        precio = item.find_element(*SELECTORES_CARRITO["precio_item"]).text
        lista_items.append({"nombre": nombre, "precio": precio})
    
    return lista_items


def capturar_pantalla(driver, nombre_archivo, carpeta="reports"):
    """Captura una screenshot y la guarda en la carpeta especificada."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_completo = f"{nombre_archivo}_{timestamp}.png"
    
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    ruta_completa = os.path.join(carpeta, nombre_completo)
    driver.save_screenshot(ruta_completa)
    
    return ruta_completa
