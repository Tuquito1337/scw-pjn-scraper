import re

PATRON_CARATULA = re.compile(
    r"(?P<demandante>.*?) C/ (?P<demandado>.*?) S/(?P<tipo_demanda>.+)"  # Caso con demandado
    r"|(?P<demandante_sin_demandado>.*?) S/(?P<tipo_demanda_sin_demandado>.+)"  # Caso sin demandado
)


# Función para limpiar el texto del demandante
def limpiar_nombre_demandante(demandante):
    """
    Limpia el nombre del demandante, eliminando detalles innecesarios como 'INCIDENTISTA' y similares.
    """
    # Eliminar 'INCIDENTISTA' y todo lo anterior al mismo
    demandante_limpio = re.sub(r".*INCIDENTISTA: ", "", demandante)
    return demandante_limpio


def extraer_datos(caratula):
    """
    Extrae los datos de la carátula, incluyendo el demandante, demandado y tipo de demanda.
    """
    match = PATRON_CARATULA.search(caratula)

    if match:
        grupos = match.groupdict()

        # Caso con demandado
        if grupos["demandante"] and grupos["demandado"]:
            return {
                "demandante": limpiar_nombre_demandante(grupos["demandante"]),
                "demandado": grupos["demandado"].strip(),
                "tipo_demanda": grupos["tipo_demanda"].strip().replace("S/", "|"),
            }

        # Caso sin demandado
        elif grupos["demandante_sin_demandado"]:
            return {
                "demandante": limpiar_nombre_demandante(
                    grupos["demandante_sin_demandado"]
                ),
                "demandado": None,
                "tipo_demanda": grupos["tipo_demanda_sin_demandado"]
                .strip()
                .replace("S/", "|"),
            }

    return None
