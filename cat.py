from flask_restful import Resource, reqparse, request
from db import db


class CatModel(db.Model):
   __tablename__ = 'categorys'
   nr = db.Column(db.Integer, primary_key=True)
   catname = db.Column(db.String(25))
   def __init__(self,newcat):
   	  self.catname = newcat
   def json(self):
   	   return {'catname': self.catname, 'nr': self.nr}
   def save_to_db(self):
   	  db.session.add(self)
   	  db.session.commit()




class Cat(Resource): 
   parser = reqparse.RequestParser()	
   parser.add_argument('newcat', 
   	required = True, 
   	help = "Kan ej lemnas blankt"
   )
   ### Insert a new category
   def post(self):
      data = Cat.parser.parse_args()
      item = CatModel(data['newcat'])
      try:
      	item.save_to_db()
      except:
      	return {"Message": "An error occured inserting the new cat to db."},500
      return item.json(), 201

   ### Delete category with <nr>
   def delete(self,nr): 
      pass

class CatList(Resource):
   ### Return all categorys   
   def get(self):
      return {'categorys': list(map(lambda x: x.json(), CatModel.query.all()))}
