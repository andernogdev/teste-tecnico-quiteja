from script.manipulador_dados import ManipuladorDados


class ConsultaTipoService:

    @staticmethod
    def consulta_tipo_por_id(id_tipo: int) -> dict:
        """Método para consultar um tipo.

        Args:
            id_tipo (int): id do tipo.

        Returns:
            dict: response da requisição.
        """
        manip_dados = ManipuladorDados()

        if not manip_dados.descompactar_arquivo("dados.zip"):
            return {
                'status': 500,
                'data': {
                    'message': 'Erro ao descompactar arquivo .zip.'
                }
            }

        if not manip_dados.carregar_arquivos_csv():
            return {
                'status': 500,
                'data': {
                    'message': 'Erro ao carregar arquivos .csv.'
                }
            }

        nome_tipo = manip_dados.obtem_tipo_por_id(id_tipo)

        if not nome_tipo:
            return {
                'status': 404,
                'data': {
                    'message': f'ID {id_tipo} não encontrado.'
                }
            }

        return {
            'status': 200,
            'data': {
                'id': id_tipo,
                'nome': nome_tipo
            }
        }
