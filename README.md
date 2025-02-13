# teste-tecnico-quiteja

## Descrição do projeto

- O projeto consiste em um script que gera inserts para popular um banco de dados PostgreSQL e um servidor Flask que disponibiliza uma API para consulta dos dados.
- Construído com Python 3.12+ no Windows 11.
- Desenvolvido com Flask e pandas.
- Servidor Flask e o script gerador de inserts podem ser executados de uma vez, mas se preferir visualizar o funcionamento separadamente, comente o trecho adequado no arquivo `main.py`.

## Como rodar o projeto

1. Clone o repositório.
2. Acesse a pasta do projeto pelo terminal.
3. Execute o comando `python -m venv .venv` para criar um ambiente virtual.
4. Execute o comando `.venv/Scripts/activate` para ativar o ambiente virtual.
5. Execute o comando `pip install -r requirements.txt` para instalar as dependências.
6. No arquivo `main.py`, comente o trecho que não deseja executar, ou execute o script e o servidor Flask de uma vez.
7. Execute o comando `python main.py` para rodar o script gerador de inserts e/ou o servidor Flask.

### Para Linux

- No passo 3, execute o comando `python3 -m venv .venv` para criar um ambiente virtual.
- No passo 4, execute o comando `source .venv/bin/activate` para ativar o ambiente virtual.
