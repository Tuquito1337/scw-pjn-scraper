from models.informe import Informe
from utils import extraer_datos
from playwright.async_api import Page


async def obtener_enlaces_expedientes(page):
    """
    Extrae los enlaces a los detalles de cada expediente judicial desde la tabla.
    """
    filas = await page.query_selector_all('table[id="j_idt118:j_idt119:dataTable"] tr')
    enlaces_expedientes = []

    for fila in filas:
        enlaces = await fila.query_selector_all("td.text-center .btn-group a")
        for enlace in enlaces:
            onclick_value = await enlace.get_attribute("onclick")
            if onclick_value:
                onclick_value = onclick_value.replace("'", "\\'").replace('"', '\\"')
                selector_unico = (
                    f'td.text-center .btn-group a[onclick="{onclick_value}"]'
                )
                enlaces_expedientes.append(selector_unico)

    return enlaces_expedientes


async def extraer_fechas_relevantes(page: Page):
    """
    Extrae las fechas relevantes relacionadas con un expediente judicial,
    excluyendo los spans que están dentro de un div.
    """
    # Seleccionar todos los spans con la clase "font-color-black"
    todos_los_spans = await page.query_selector_all(
        'table[id="expediente:action-table"] tbody tr span.font-color-black, '
        'table[id="expediente:action-table"] tbody tr span.font-negrita'
    )

    # Filtrar solo los spans que no estén dentro de un <div>
    filas = [
        span
        for span in todos_los_spans
        if not await span.evaluate(
            '(element) => element.parentElement.tagName.toLowerCase() === "div"'
        )
    ]

    # Agrupar las fechas relevantes en diccionarios
    return [
        {
            "Fecha": (await filas[i].inner_text()),
            "Tipo": (await filas[i + 1].inner_text()),
            "Detalle": (await filas[i + 2].inner_text()),
        }
        for i in range(0, len(filas), 3)
    ]


async def obtener_datos_expediente(page):
    """
    Extrae los datos principales de un expediente judicial.
    """
    # Extraer datos de la página
    expediente = await page.inner_text(
        'div[class="col-xs-10 col-sm-10 col-md-10 col-lg-10"] span[style="color:#000000;"] '
    )
    jurisdiccion = await page.inner_text('span[id="expediente:j_idt90:detailCamera"]')
    situacion_actual = await page.inner_text(
        'span[id="expediente:j_idt90:detailSituation"]'
    )
    dependencia = await page.inner_text(
        'span[id="expediente:j_idt90:detailDependencia"]'
    )
    caratula = await page.inner_text('span[id="expediente:j_idt90:detailCover"]')

    # Extraer fechas relevantes
    fechas_relevantes = await extraer_fechas_relevantes(page)

    # Procesar la carátula para obtener demandante, demandado y tipo de demanda
    datos_caratula = extraer_datos(caratula)

    # Crear el informe con los datos extraídos
    informe_expediente = Informe(
        expediente=expediente,
        jurisdiccion=jurisdiccion,
        situacion_actual=situacion_actual,
        dependencia=dependencia,
        demandante=datos_caratula["demandante"],
        demandado=datos_caratula["demandado"],
        caratula=caratula,
        fechas_relevantes=fechas_relevantes,
        juzgado=dependencia,
        tipo_demanda=datos_caratula["tipo_demanda"],
    )

    return informe_expediente
