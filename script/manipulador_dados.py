import os
from zipfile import ZipFile
import pandas as pd


class ManipuladorDados:

    PATH_DADOS = "./script"
    ARQUIVOS_CSV = [
        "origem-dados.csv",
        "tipos.csv"
    ]

    def __init__(self) -> None:
        self.__df_origem_dados = None
        self.__df_tipos = None

    @property
    def df_origem_dados(self) -> pd.DataFrame:
        """DataFrame dos dados de origem."""
        return self.__df_origem_dados

    @property
    def df_tipos(self) -> pd.DataFrame:
        """DataFrame dos tipos."""
        return self.__df_tipos

    def ordenar_filtrar_dados(self) -> bool:
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

    def carrega_tipos(self):
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
            # print('Arquivos já descompactados.')
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
