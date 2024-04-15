from flask import Flask
from BackEnd.college_predictor_results import college_predictor

app = Flask(__name__, template_folder='FrontEnd/templates', static_folder='FrontEnd/static')

from sanic import Sanic
from sanic.response import json
app = Sanic()

app.register_blueprint(college_predictor)


