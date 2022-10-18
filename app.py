from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

fakeDatabase = {
    1: {'name': 'Clean car'},
    2: {'name': 'Write blog'},
    3: {'name': 'Start stream'},
}


class Items(Resource):
    def get(self):
        return fakeDatabase


class Item(Resource):
    def get(self, pk):
        return fakeDatabase[pk]


api.add_resource(Items, '/')
api.add_resource(Item, '/<int:pk>')

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run(debug=True)
