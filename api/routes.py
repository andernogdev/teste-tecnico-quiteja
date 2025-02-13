from flask import Flask
from api.view.consulta_tipo_controller import TipoController


app = Flask(__name__)


# Registra a rota do controller no app Flask da aplicação
TipoController.register(app, route_base = '/tipo')
