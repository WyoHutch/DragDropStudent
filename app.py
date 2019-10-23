from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
import os

app = Flask(__name__)
heroku = Heroku(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://iqiszpzxrnecrl:82b0c1758a3ab17a0e8adcd666f52c939e0224bd25625304d6ee2e97e273b754@ec2-174-129-241-114.compute-1.amazonaws.com:5432/dbhr6c772m4dtj"

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique = False)
    team = db.Column(db.String(20), unique = False)

    def __init__(self, name, team):
        self.name = name
        self.team = team

class StudentSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "team")

single_jschema = StudentSchema()
plural_jschema = StudentSchema(many = True)

@app.route('/students', methods=['GET'])
def get_Students():
    all_students = Student.query.all()
    return jsonify(plural_jschema.dump(all_students))

@app.route('/getStudent/<id>', methods=['GET'])
def return_student(id):
    student = Student.query.get(id)
    return jsonify(single_jschema.dump(student))

@app.route('/student', methods=['POST'])
def add_student():
    name = request.json["name"]
    team = request.json["team"]

    new_student = Student(name, team)

    db.session.add(new_student)
    db.session.commit()

    return single_jschema.jsonify(Student.query.get(new_student.id))

@app.route('/student/<id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)

    student.name = request.json('name')
    student.team = request.json('team')

    db.session.commit()
    return single_jschema.jsonify(student)

@app.route('/delStudent/<id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()

    all_students = Student.query.all()
    return jsonify(plural_jschema.dump(all_students))

if __name__ == '__main__':
    app.run(debug = True)