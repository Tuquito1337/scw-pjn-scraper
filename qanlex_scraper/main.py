import logging
import asyncio
from playwright.async_api import async_playwright, Page
from captcha_solver import resolve_captcha
from config import palabra_clave, base_url, headless_option
from data_extractor import obtener_datos_expediente, obtener_enlaces_expedientes

# Configuración básica del logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("scraping_log.log"),  # Guardar log en un archivo
    ],
)
logger = logging.getLogger(__name__)


from services.informe_service import upsert_execute


async def resolver_captcha(page: Page, url: str):
    """
    Obtiene el sitekey y resuelve el CAPTCHA.
    """
    logging.info("Resolviendo CAPTCHA...")
    sitekey = await page.get_attribute('div[class*="g-recaptcha"]', "data-sitekey")
    if not sitekey:
        raise Exception("No se encontró el sitekey del CAPTCHA.")
    captcha_solution = resolve_captcha(url, sitekey)
    await page.evaluate(
        f'document.getElementById("g-recaptcha-response").value="{captcha_solution}";'
    )
    logging.info("CAPTCHA resuelto exitosamente.")


async def completar_y_enviar_formulario(page: Page):
    """
    Completa el formulario de búsqueda y lo envía.
    """
    logging.info("Completando y enviando formulario...")
    await page.select_option('select[id="formPublica:camaraPartes"]', "10")
    await page.fill('input[id="formPublica:nomIntervParte"]', palabra_clave)
    await page.click('input[id="formPublica:buscarPorParteButton"]')
    await page.wait_for_load_state()
    logging.info("Formulario enviado.")


async def procesar_expedientes(page: Page):
    """
    Obtiene enlaces de expedientes y procesa cada uno.
    Luego, si encuentra el botón de siguiente página, navega a la siguiente.
    """
    while True:
        # Obtener enlaces de expedientes en la página actual
        enlaces = await obtener_enlaces_expedientes(page)
        if not enlaces:
            logging.info("No se encontraron expedientes en la página actual.")
            break

        for index, enlace_selector in enumerate(enlaces):
            try:
                logging.info(f"Procesando expediente {index + 1}...")
                await page.click(enlace_selector)
                informe = await obtener_datos_expediente(page)
                await asyncio.to_thread(upsert_execute, informe)
                await page.go_back()  # Volver a la página anterior
                await page.wait_for_load_state()
            except Exception as e:
                logging.error(f"Error procesando expediente {index + 1}: {e}")

        # Buscar el botón para ir a la siguiente página
        try:
            siguiente_pagina_btn = await page.query_selector(
                'a[id="j_idt118:j_idt208:j_idt215"]'
            )
            if siguiente_pagina_btn:
                logging.info("Encontrado botón de siguiente página, haciendo clic...")
                await siguiente_pagina_btn.click()
                await page.wait_for_load_state()
            else:
                logging.info(
                    "No se encontró el botón de siguiente página, terminando el scrapeo."
                )
                break
        except Exception as e:
            logging.error(f"Error al intentar navegar a la siguiente página: {e}")
            break


async def scrape_expedientes(base_url: str, headless=True):
    """
    Función principal que maneja todo el proceso de scraping.
    """
    logging.info("Iniciando la scraping...")
    try:
        # Inicializar navegador y contexto
        async with async_playwright() as p:
            logging.info("Iniciando navegador...")
            browser = await p.chromium.launch(headless=headless)
            context = await browser.new_context()
            page = await context.new_page()
            logging.info("Iniciando página...")
            await page.goto(base_url)

            # Activar el formulario
            await page.click('td[id="formPublica:porParte:header:inactive"]')

            # Resolver CAPTCHA y completar el formulario
            await resolver_captcha(page, base_url)
            await completar_y_enviar_formulario(page)

            # Procesar los expedientes
            await procesar_expedientes(page)

    except Exception as e:
        logging.exception(f"Error durante el scraping: {e}")
    finally:
        if browser:
            await browser.close()
            logging.info("Navegador cerrado.")


if __name__ == "__main__":
    asyncio.run(scrape_expedientes(base_url=base_url, headless=headless_option))
