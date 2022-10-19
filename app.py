from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)


app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return self.name


with app.app_context():
    db.create_all()

fakeDatabase = {
    1: {'name': 'Clean car'},
    2: {'name': 'Write blog'},
    3: {'name': 'Start stream'},
}

taskFiedls = {
    'id': fields.Integer,
    'name': fields.String
}


class Items(Resource):
    @marshal_with(taskFiedls)
    def get(self):
        tasks = Task.query.all()
        return tasks

    @marshal_with(taskFiedls)
    def post(self):
        data = request.json
        task = Task(name=data['name'])
        db.session.add(task)
        db.session.commit()
        # itemId = len(fakeDatabase.keys()) + 1
        # fakeDatabase[itemId] = {'name': data['name']}
        tasks = Task.query.all()
        return tasks


class Item(Resource):
    def get(self, pk):
        task = Task.query.filter_by(id=pk).first()
        return fakeDatabase[pk]

    def put(self, pk):
        data = request.json
        fakeDatabase[pk]['name'] = data['name']

        return fakeDatabase

    def delete(self, pk):
        del fakeDatabase[pk]
        return fakeDatabase


api.add_resource(Items, '/')
api.add_resource(Item, '/<int:pk>')

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run(debug=True)
