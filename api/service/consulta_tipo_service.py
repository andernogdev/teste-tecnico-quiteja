from script.gerador_inserts import GeradorInserts


class ConsultaTipoService:

    @staticmethod
    def consulta_tipo_por_id(id_tipo: int) -> dict:
        """Método para consultar um tipo.

        Args:
            id_tipo (int): id do tipo.

        Returns:
            dict: response da requisição.
        """
        gerador_inserts = GeradorInserts()

        if not gerador_inserts.descompactar_arquivo("dados.zip"):
            return {
                'status': 500,
                'data': {
                    'message': 'Erro ao descompactar arquivo .zip.'
                }
            }

        if not gerador_inserts.carregar_arquivos_csv():
            return {
                'status': 500,
                'data': {
                    'message': 'Erro ao carregar arquivos .csv.'
                }
            }

        descricao_tipo = gerador_inserts.obtem_tipo_por_id(id_tipo)

        if not descricao_tipo:
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
                'descricao': descricao_tipo
            }
        }
