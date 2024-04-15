from flask import Flask
from BackEnd.college_predictor_results import college_predictor

app = Flask(__name__, template_folder='FrontEnd/templates', static_folder='FrontEnd/static')

app.register_blueprint(college_predictor)


if __name__ == '__main__':
  app.run(debug=True)
