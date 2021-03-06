from flask import Flask, request
from flask_restful import Resource, Api
# Local resources
import login
from cat import Cat, CatList
from quest import NewQuest, Quest
from game import NewGame, EndGame, Scores

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = login.mysql['uri']
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + login.dbuser['username'] + ':' + login.dbuser['password'] + login.dbuser['database']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
@app.before_first_request
def create_tables():
	db.create_all()

class Ping(Resource):
   def get(self):
    return {'message': 'Pong'}

api.add_resource(NewQuest, '/newquest')
api.add_resource(Quest, '/quest/<int:nr>')
api.add_resource(Cat, '/cat')
api.add_resource(CatList, '/catlist')
api.add_resource(NewGame, '/newgame')
api.add_resource(EndGame, '/endgame')
api.add_resource(Scores, '/scores')
api.add_resource(Ping, '/ping')



if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5000, debug=True)
