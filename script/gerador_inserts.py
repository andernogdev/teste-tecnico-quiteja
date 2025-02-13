import os
from zipfile import ZipFile
import pandas as pd


class GeradorInserts:

    PATH_DADOS = "./script"
    ARQUIVOS_CSV = [
        "origem-dados.csv",
        "tipos.csv"
    ]

    def __init__(self) -> None:
        self.__df_origem_dados = None
        self.__df_tipos = None

    def __ordenar_filtrar_dados(self) -> bool:
        """Efetua a ordenação dos dados e filtra apenas
            os registros com status "CRITICO".

        Returns:
            bool: True se a operação for bem sucedida, False caso contrário.
        """
        if self.__df_origem_dados.empty:
            print("DataFrame de dados não carregado.")
            return False

        # Filtro que seleciona apenas os registros com status "CRITICO"
        self.__df_origem_dados = self.__df_origem_dados[
            self.__df_origem_dados['status'] == "CRITICO"
        ]

        # [X] Crescente ou [ ] decrescente (?)
        self.__df_origem_dados = self.__df_origem_dados.sort_values(
            by = "created_at",
            ascending = True
        )

        return True

    def __carrega_tipos(self):
        """Carrega a descrição do tipo de cada registro.

        Returns:
            bool: True se a operação for bem sucedida, False caso contrário.
        """
        if self.__df_tipos.empty:
            print("DataFrame de tipos não carregado.")
            return False

        self.__df_origem_dados['descricao_tipo'] = self.__df_origem_dados['tipo'].map(
            self.__df_tipos.set_index('id')['nome']
        )

        return True

    def __gerar_inserts_sql(self) -> bool:
        # Geração das queries de insert
        for idx, row in self.__df_origem_dados.iterrows():
            self.__df_origem_dados.loc[idx, 'insert'] = (
                "INSERT INTO dados_finais "
                "(created_at, product_code, customer_code, status, tipo) "
                "VALUES ("
                f"TIMESTAMP '{row['created_at']}', "
                f"{row['product_code']}, "
                f"{row['customer_code']}, "
                f"'{row['status']}', "
                f"'{row['descricao_tipo']}');"
            )

        # Geração do arquivo insert-dados.sql
        self.__df_origem_dados.to_csv(
            f"{self.PATH_DADOS}/insert-dados.sql",
            columns = ['insert'],
            header = False,
            index = False
        )

        return True

    def __gerar_query_sql(self) -> str:
        # com base na estrutura desta tabela,
        # monte uma query que retorne, por dia,
        # a quantidade de itens agrupadas pelo tipo;
        query_select = (
            "SELECT "
                "created_at::DATE AS date_created_at, "
                "tipo, "
                "COUNT(*) AS quantidade "
            "FROM dados_finais "
            "GROUP BY date_created_at, tipo "
            "ORDER BY date_created_at, tipo;"
        )

        return query_select

    def descompactar_arquivo(self, nome_arquivo_zip: str) -> bool:
        """Descompacta o arquivo zip com os dados de origem.

        Args:
            nome_arquivo_zip (str): Nome do arquivo zip a ser descompactado.

        Returns:
            bool: True se a operação for bem sucedida, False caso contrário.
        """
        arquivos_diretorio_script = os.listdir(self.PATH_DADOS)

        # Verifica se os arquivos já foram descompactados
        if (any(
            arquivo in self.ARQUIVOS_CSV
            for arquivo in arquivos_diretorio_script
        )):
            print('Arquivos já descompactados.')
            return True

        # Descompacta o arquivo zip
        try:
            with (ZipFile(
                file = f"{self.PATH_DADOS}/{nome_arquivo_zip}",
                mode = 'r'
            ) as zip_ref):
                zip_ref.extractall(self.PATH_DADOS)

        except Exception as e:
            print(f"Erro ao descompactar arquivo: {e}")

            # Exibe os arquivos do diretório /script
            print(f"Arquivos no diretório {self.PATH_DADOS}:")
            print(os.listdir(self.PATH_DADOS))

            return False

        return True

    def carregar_arquivos_csv(self) -> bool:
        """Carrega os arquivos CSV de origem dos dados e os tipos.

        Returns:
            bool: True se a operação for bem sucedida, False caso contrário.
        """
        # Carrega os arquivos CSV
        try:
            self.__df_origem_dados = pd.read_csv(
                f"{self.PATH_DADOS}/{self.ARQUIVOS_CSV[0]}"
            )

            self.__df_tipos = pd.read_csv(
                f"{self.PATH_DADOS}/{self.ARQUIVOS_CSV[1]}"
            )

        except Exception as e:
            print(f"Erro ao carregar arquivos CSV: {e}")
            return False

        return True

    def obtem_tipo_por_id(self, id_tipo: int) -> str:
        """Obtém a descrição do tipo pelo id.

        Args:
            id_tipo (int): id do tipo consultado.

        Returns:
            str: Descrição do tipo.
        """
        tipo = self.__df_tipos.loc[
            self.__df_tipos['id'] == id_tipo,
            'nome'
        ]

        return tipo.values[0] if not tipo.empty else None

    def executar(self):
        """Executa o script que efetua a descompactação do arquivo .zip
            leitura dos arquivos .csv descompactados, tratamento dos dados
            geração dos inserts SQL e, ao final, a query de consulta.
        """
        if not self.descompactar_arquivo("dados.zip"):
            return

        if not self.carregar_arquivos_csv():
            return

        if not self.__ordenar_filtrar_dados():
            return

        if not self.__carrega_tipos():
            return

        if not self.__gerar_inserts_sql():
            return

        print("\n<QUERY>")
        print(self.__gerar_query_sql())
        print("</QUERY>\n")
