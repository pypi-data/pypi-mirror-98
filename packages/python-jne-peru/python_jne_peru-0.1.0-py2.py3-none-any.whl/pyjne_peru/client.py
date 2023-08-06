import requests

from .parsers import EntityParser
from .error import JNEException


class JNE:
    """
    Plataforma Electoral JNE API
    """

    def __init__(self, parser=None):
        self.base_url = "https://plataformaelectoral.jne.gob.pe"
        self.parser = parser or EntityParser()

    def _build_url(self, path):
        return f"{self.base_url}{path}"

    def _make_request(self, method, path, payload_type=None, payload_list=False,
                      post_data=None, params=None, **kwargs):
        request_method = requests.post if method == "POST" else requests.get
        response = request_method(self._build_url(path), params=params or {}, data=post_data or {})
        if response.status_code != 200:
            raise JNEException(f"JNE error response: status code = {response.status_code}")

        result = self.parser.parse(response.json(), payload_list=payload_list, payload_type=payload_type)
        return result

    def get_electoral_districts(self):
        """
        Note: Este metodo no devuelve todos los distritos electorales disponibles.
        Por ejemplo. PERUANOS RESIDENTES EN EL EXTERIOR (140101)
        """
        return self._make_request(
            "GET", "/Candidato/ListUbigeoDepartamento",
            payload_type="electoral_district", payload_list=True)

    def get_election_processes(self):
        return self._make_request(
            "GET", "/Resoluciones/GetListProcesosCR",
        payload_type="election_process", payload_list=True)

    def get_election_types_by_process(self, proceso_electoral: int):
        return self._make_request(
            "GET", f"/Candidato/GetTipoEleccionbyProceso/{proceso_electoral}",
            payload_type="election_type", payload_list=True)

    def get_files(self, jurado_electoral: int = 0, organizacion_politica: int = 0,
                        proceso_electoral: int = 0, tipo_expediente: int = 0, ubigeo: str = "000000"):
        return self._make_request(
            "POST", "/Expediente/BusquedaReporteAvanzadoExpediente",
            payload_type="file", payload_list=True,
            post_data={
                "idJuradoElectoral": jurado_electoral,
                "idOrganizacionPolitica": organizacion_politica,
                "idProcesoElectoral": proceso_electoral,
                "idTipoExpediente": tipo_expediente,
                "strUbigeo": ubigeo
            })

    def get_files_on_list(self, proceso_electoral: int, tipo_eleccion: int,
                          jurado_electoral: int = 0, distrito_electoral: int = 0):
        if not distrito_electoral:
            distrito_electoral = "null"
        path = f"/Candidato/GetExpedientesLista/" \
               f"{proceso_electoral}-{tipo_eleccion}-{distrito_electoral}------{jurado_electoral}-"
        return self._make_request(
            "GET", path,
            payload_type="file", payload_list=True,
        )

    def get_file(self, cod_expediente_ext: str):
        return self._make_request(
            "POST", "/Expediente/BuscandoCodigo",
            payload_type="file_extended", payload_list=False,
            post_data={
                "strNumExpedienteFiltro": cod_expediente_ext
            }
        )

    def get_candidates_by_list(self, proceso_electoral: int, tipo_eleccion: int,
                               id_solicitud: int, id_expediente: int):
        path = f"/Candidato/GetCandidatos/{tipo_eleccion}-{proceso_electoral}-{id_solicitud}-{id_expediente}"
        return self._make_request(
            "GET", path, payload_type="candidate", payload_list=True
        )

    def get_resume(self, id_hoja_vida: int, proceso_electoral: int,
                               id_organizacion_poitica: int):
        params = {
            "param": f"{id_hoja_vida}-0-{id_organizacion_poitica}-{proceso_electoral}"
        }
        return self._make_request(
            "GET", "/HojaVida/GetHVConsolidado", params=params, payload_type="resume",
            payload_list=False
        )
