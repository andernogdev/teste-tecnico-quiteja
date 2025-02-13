from flask_classful import FlaskView, route, make_response
from api.service.consulta_tipo_service import ConsultaTipoService


class TipoController(FlaskView):

    route_base = 'tipo'

    @route('/<int:id_tipo>', methods=['GET'])
    def consultar_tipo_por_id(self, id_tipo: int) -> dict:
        """Rota para consultar a descrição do tipo do id informado.

        Args:
            id_tipo (int): id a ser consultado.

        Returns:
            dict: response da requisição.
        """
        # print(f"Consultando tipo do id {id_tipo}...")

        response = ConsultaTipoService().consulta_tipo_por_id(id_tipo)

        return make_response(response['data'], response['status'])
