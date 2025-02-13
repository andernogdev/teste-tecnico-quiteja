from api.routes import app
from script.gerador_inserts import GeradorInserts

if __name__ == '__main__':
    # Descomentar para executar o script
    gerador_inserts = GeradorInserts()
    gerador_inserts.executar()

    # Descomentar para rodar a API
    app.run(debug = False)
