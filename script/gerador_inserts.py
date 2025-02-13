from script.manipulador_dados import ManipuladorDados


class GeradorInserts:

    NOME_ARQUIVO_SQL = "insert-dados.sql"

    def __init__(self) -> None:
        self.manip_dados = ManipuladorDados()

    def __gerar_inserts_sql(self) -> bool:
        # Geração das queries de insert
        for idx, row in self.manip_dados.df_origem_dados.iterrows():
            self.manip_dados.df_origem_dados.loc[idx, 'insert'] = (
                "INSERT INTO dados_finais "
                "(created_at, product_code, customer_code, status, tipo) "
                "VALUES ("
                f"TIMESTAMP '{row['created_at']}', "
                f"{row['product_code']}, "
                f"{row['customer_code']}, "
                f"'{row['status']}', "
                f"'{row['nome_tipo']}');"
            )

        nome_arquivo_sql = f"{self.manip_dados.PATH_DADOS}/{self.NOME_ARQUIVO_SQL}"

        try:
            # Geração do arquivo insert-dados.sql
            self.manip_dados.df_origem_dados.to_csv(
                nome_arquivo_sql,
                columns = ['insert'],
                header = False,
                index = False
            )

            # Remove " do arquivo insert-dados.sql
            with open(
                file = nome_arquivo_sql,
                mode = 'r',
                encoding = "UTF-8"
            ) as f_read:
                data = f_read.read()

                with open(
                    file = nome_arquivo_sql,
                    mode = 'w',
                    encoding = "UTF-8"
                ) as f_write:
                    f_write.write(data.replace('"', ''))
        except Exception as e:
            print(f"Erro ao gerar arquivo {nome_arquivo_sql}: {e}")
            return False

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

    def executar(self):
        """Executa o script que efetua a descompactação do arquivo .zip
            leitura dos arquivos .csv descompactados, tratamento dos dados
            geração dos inserts SQL e, ao final, a query de consulta.
        """
        if not self.manip_dados.descompactar_arquivo("dados.zip"):
            return

        if not self.manip_dados.carregar_arquivos_csv():
            return

        if not self.manip_dados.ordenar_filtrar_dados():
            return

        if not self.manip_dados.carrega_tipos():
            return

        if not self.__gerar_inserts_sql():
            return

        print("\n<QUERY>")
        print(self.__gerar_query_sql())
        print("</QUERY>\n")
