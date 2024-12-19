class Informe:
    """
    Clase que representa un informe legal de un expediente judicial.
    """

    def __init__(
        self,
        expediente=None,
        jurisdiccion=None,
        situacion_actual=None,
        dependencia=None,
        demandante=None,
        demandado=None,
        caratula=None,
        tipo_demanda=None,
        juzgado=None,
        fechas_relevantes=None,
    ):
        self.expediente = expediente
        self.jurisdiccion = jurisdiccion
        self.situacion_actual = situacion_actual
        self.dependencia = dependencia
        self.demandante = demandante
        self.demandado = demandado
        self.caratula = caratula
        self.tipo_demanda = tipo_demanda
        self.juzgado = juzgado
        self.fechas_relevantes = fechas_relevantes or []

    def _set(self, atributo, valor):
        """Método genérico para establecer o actualizar un atributo."""
        if isinstance(valor, str) and valor.strip():
            setattr(self, atributo, valor)
        else:
            raise ValueError(f"El valor de {atributo} debe ser una cadena no vacía.")

    def set_expediente(self, expediente):
        self._set("expediente", expediente)

    def set_dependencia(self, dependencia):
        self._set("dependencia", dependencia)

    def set_demandante(self, demandante):
        self._set("demandante", demandante)

    def set_demandado(self, demandado):
        self._set("demandado", demandado)

    def set_caratula(self, caratula):
        self._set("caratula", caratula)

    def set_tipo_demanda(self, tipo_demanda):
        self._set("tipo_demanda", tipo_demanda)

    def set_juzgado(self, juzgado):
        self._set("juzgado", juzgado)

    def set_jurisdiccion(self, jurisdiccion):
        self._set("jurisdiccion", jurisdiccion)

    def set_situacion_actual(self, situacion_actual):
        self._set("situacion_actual", situacion_actual)

    def set_fecha_relevante(self, fecha):
        """Agregar una fecha relevante al informe."""
        if isinstance(fecha, dict):
            self.fechas_relevantes.append(fecha)
        else:
            print("Por favor, ingrese una fecha válida.")

    # Métodos GET
    def get_expediente(self):
        return self.expediente

    def get_dependencia(self):
        return self.dependencia

    def get_demandante(self):
        return self.demandante

    def get_demandado(self):
        return self.demandado

    def get_caratula(self):
        return self.caratula

    def get_tipo_demanda(self):
        return self.tipo_demanda

    def get_juzgado(self):
        return self.juzgado

    def get_jurisdiccion(self):
        return self.jurisdiccion

    def get_situacion_actual(self):
        return self.situacion_actual

    def get_fechas_relevantes(self):
        return self.fechas_relevantes

    def mostrar_informe(self):
        """Mostrar la información del informe de forma legible."""
        return f"""
Expediente: {self.expediente or 'N/A'}
Jurisdicción: {self.jurisdiccion or 'N/A'}
Situación Actual: {self.situacion_actual or 'N/A'}
Dependencia: {self.dependencia or 'N/A'}
Demandante: {self.demandante or 'N/A'}
Demandado: {self.demandado or 'N/A'}
Carátula: {self.caratula or 'N/A'}
Tipo de Demanda: {self.tipo_demanda or 'N/A'}
Juzgado: {self.juzgado or 'N/A'}
Fechas Relevantes: {self.fechas_relevantes or 'N/A'}
"""
