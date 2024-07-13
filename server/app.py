from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        message_dict_list = [message.to_dict() for message in Message.query.all()]
        response = make_response(message_dict_list, 200)
        return response
    elif request.method == 'POST':
        new_message = Message(
            username = request.get_json()['username'],
            body = request.get_json()['body']
        )

        db.session.add(new_message)
        db.session.commit()

        response = make_response(new_message.to_dict(), 201)
        return response

@app.route('/messages/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    if request.method == 'GET':
        message = Message.query.filter_by(id = id).first().to_dict()
        response = make_response(message, 200)
        return response
    elif request.method == 'PATCH':
        data = request.get_json()
        message = Message.query.filter_by(id = id).first()
        for attr in data:
          setattr(message, attr, data[attr])

        db.session.add(message)
        db.session.commit()

        response = make_response(message.to_dict(), 200)
        return response
    elif request.method == 'DELETE':
        message = Message.query.filter_by(id = id).first()
        db.session.delete(message)
        db.session.commit()

        response = make_response({
            "delete_sucessfull" : True,
            "Message" : "Deleted sucessfully"
        }, 200)
    

if __name__ == '__main__':
    app.run(port=5555)
