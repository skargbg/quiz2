from flask_restful import Resource, reqparse, request
from flask import jsonify
from db import db
from quest import QuestModel


class GameModel(db.Model):
   pass
   __tablename__ = 'games'
   nr = db.Column(db.Integer, primary_key=True)
   player = db.Column(db.String(25))
   cat = db.Column(db.Integer)
   count = db.Column(db.Integer)
   result = db.Column(db.Integer)
   def __init__(self,player,category,count):
        self.player = player
        self.cat = category
        self.count = count
        self.result = -1
   def json(self):
   	   return {'nr': self.nr, 'player': self.player, 'category': self.cat, 'count': self.count, 'result': self.result}
   def save_to_db(self):
   	  db.session.add(self)
   	  db.session.commit()
   @classmethod
   def find_by_nr(cls,_nr):
      return cls.query.filter_by(nr=_nr).first()

class NewGame(Resource): 
   parser = reqparse.RequestParser()   
   parser.add_argument('player', 
      required = True, 
      help = "Kan ej lemnas blankt (player)"
   )
   parser.add_argument('category',
      type=int, 
      required = True, 
      help = "Kan ej lemnas blankt (category)"
   )
   parser.add_argument('count', 
      type=int, 
      required = True, 
      help = "Kan ej lemnas blankt (count)"
   )
   def post(self):
      data = NewGame.parser.parse_args()
      item = GameModel(data['player'], data['category'], data['count'])
      questlist=QuestModel.quest_by_cat(str(item.cat), item.count)
      result = []
      for i in questlist:
         result.append(i.nr)
      try:
         item.save_to_db()
      except:
         return {"Message": "An error occured creating new game in db."},500
      return jsonify(questlist=result)

class EndGame(Resource): 
   parser = reqparse.RequestParser()   
   parser.add_argument('nr',
      type=int, 
      required = True, 
      help = "Kan ej lemnas blankt (nr)"
   )
   parser.add_argument('correct', 
      type=int, 
      required = True, 
      help = "Kan ej lemnas blankt (correct)"
   )
   def put(self):
      data = EndGame.parser.parse_args()
      item = GameModel.find_by_nr(data['nr'])
      if item:
         item.result=data['correct']
         item.save_to_db()
         return item.json(), 201
      return {"Message": "Error writing result to db."},500
      



class Scores(Resource):
   ### Return all scores   
   def get(self):
      return {'scores': list(map(lambda x: x.json(), GameModel.query.all()))}
