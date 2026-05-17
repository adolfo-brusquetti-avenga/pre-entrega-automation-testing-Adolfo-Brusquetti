# -*- coding: utf-8 -*-
"""
Configuracion de Pytest - Fixtures y Hooks
==========================================
Configuracion global de Pytest incluyendo:
- Fixture del WebDriver (Chrome)
- Configuracion de screenshots en fallos
- Hooks para reportes
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
from datetime import datetime


# ==================== CONFIGURACION DEL DRIVER ====================

@pytest.fixture(scope="function")
def driver():
    """
    Fixture que proporciona una instancia del WebDriver de Chrome.
    
    - Maximiza la ventana del navegador
    - Espera implicita de 10 segundos
    - Limpieza automatica al finalizar cada test
    """
    chrome_options = Options()
    
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-infobars")
    
    # Descomentar para modo headless (sin interfaz grafica)
    # chrome_options.add_argument("--headless")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()


# ==================== HOOKS PARA SCREENSHOTS EN FALLOS ====================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para capturar screenshots automaticamente en caso de fallo."""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        
        if driver:
            reports_dir = os.path.join(os.path.dirname(__file__), "reports")
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name
            screenshot_path = os.path.join(reports_dir, f"FALLO_{test_name}_{timestamp}.png")
            
            try:
                driver.save_screenshot(screenshot_path)
                print(f"\nScreenshot guardado: {screenshot_path}")
            except Exception as e:
                print(f"\nNo se pudo guardar screenshot: {e}")


# ==================== CONFIGURACION DE PYTEST ====================

def pytest_configure(config):
    """Agrega marcadores personalizados."""
    config.addinivalue_line("markers", "login: Tests de login")
    config.addinivalue_line("markers", "catalogo: Tests de catalogo")
    config.addinivalue_line("markers", "carrito: Tests de carrito")


def pytest_html_report_title(report):
    """Personaliza el titulo del reporte HTML."""
    report.title = "Reporte de Pruebas - Pre-Entrega Automatizacion QA"
