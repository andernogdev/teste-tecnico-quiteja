# teste-tecnico-quiteja

## Descrição do projeto

- O projeto consiste em um script que gera inserts para popular um banco de dados SQLite e um servidor Flask que disponibiliza uma API para consulta dos dados.
- Construído com Python 3.12+ no Windows 11.
- Desenvolvido com Flask e pandas.

## Como rodar o projeto

1. Clone o repositório.
2. Acesse a pasta do projeto pelo terminal.
3. Execute o comando `python -m venv .venv` para criar um ambiente virtual.
4. Execute o comando `.venv/Scripts/activate` para ativar o ambiente virtual.
5. Execute o comando `pip install -r requirements.txt` para instalar as dependências.
6. No arquivo `main.py` descomente as linhas adequadas para executar o script gerador de inserts.
7. No arquivo `main.py` descomente as linhas adequadas para executar o servidor Flask (comente as linhas do gerador de inserts antes, se preferir).

### Para Linux

- No passo 3, execute o comando `python3 -m venv .venv` para criar um ambiente virtual.
- No passo 4, execute o comando `source .venv/bin/activate` para ativar o ambiente virtual.
