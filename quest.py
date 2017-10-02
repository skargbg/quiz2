from flask_restful import Resource, reqparse, request
from sqlalchemy.sql import func
from db import db


class QuestModel(db.Model):
   __tablename__ = 'questions'
   nr = db.Column(db.Integer, primary_key=True)
   question = db.Column(db.String(250))
   answers = db.Column(db.String(400))
   category = db.Column(db.Integer)
   def __init__(self,question,answers,category):
        self.question = question
        self.answers = answers
        self.category = category
   def json(self):
   	   return {'question': self.question, 'nr': self.nr, 'answers': self.answers}
   def save_to_db(self):
   	  db.session.add(self)
   	  db.session.commit()
   @classmethod
   def find_by_nr(cls, _nr):
      return cls.query.filter_by(nr=_nr).first()
   @classmethod
   def quest_by_cat(cls,_cat,_lim):
      return cls.query.filter_by(category=_cat).order_by(func.rand()).limit(_lim).all()


class NewQuest(Resource): 
   parser = reqparse.RequestParser()	
   parser.add_argument('question', 
   	required = True, 
   	help = "Kan ej lemnas blankt (question)"
   )
   parser.add_argument('answers', 
      required = True, 
      help = "Kan ej lemnas blankt (answers)"
   )
   parser.add_argument('category',
      type=int, 
      required = True, 
      help = "Kan ej lemnas blankt (category)"
   )
   ### Insert a new question
   def post(self):
      data = NewQuest.parser.parse_args()
      item = QuestModel(data['question'], data['answers'], data['category'])
      try:
      	item.save_to_db()
      except:
      	return {"Message": "An error occured inserting the new question to db."},500
      return item.json(), 201

   ### Delete category with <nr>
#   def delete(self): 
#      pass

class Quest(Resource):
   def get(self, nr):
      item = QuestModel.find_by_nr(nr)
      if item:
         return item.json()
      return {'message': 'Question no found'}, 404

