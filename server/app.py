#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)
# After initializing app
CORS(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return [plant.to_dict() for plant in plants], 200
    
    def post(self):
        data = request.get_json()
        try:
            new_plant = Plant(
                name=data["name"],
                image=data["image"],
                price=float(data["price"]),
            )
            db.session.add(new_plant)
            db.session.commit()
            return new_plant.to_dict(), 201
        except Exception as e:
            return {"error": str(e)}, 400
            
class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if plant:
            return plant.to_dict(), 200
        return {"error": "Plant not found"}, 404
    def patch(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return {"error": "Plant not found"}, 404
        
        data = request.get_json()
        try:
            for field in ["name", "image", "price"]:
                if field in data:
                    setattr(plant, field, data[field])
            db.session.commit()
            return plant.to_dict(), 200
        except Exception as e:
            return {"error": str(e)}, 400
        
    def delete(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return {"error": "Plant not found"}, 404

        db.session.delete(plant)
        db.session.commit()
        return {}, 204

    
api.add_resource(Plants, "/plants")
api.add_resource(PlantByID, "/plants/<int:id>")
     

if __name__ == '__main__':
    app.run(port=5555, debug=True)
