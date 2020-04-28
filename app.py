from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
from flask_celery import make_celery
import time


# the app is an instance of the Flask class
app = Flask(__name__)
app.config['SECRET_KEY'] = 'there is no secret'

# app.config.update takes the following parameters:
# CELERY_BROKER_URL is the URL where the message broker (RabbitMQ) is running
# CELERY_RESULT_BACKEND is required to keep track of task and store the status
app.config.update(
CELERY_BROKER_URL = 'amqp://localhost//',  
CELERY_RESULT_BACKEND='rpc://'
)

# integrates Flask-SocketIO with the Flask application
socketio = SocketIO(app, message_queue='amqp://')

# the app is passed to meke_celery function, this function sets up celery in order to integrate with the flask application
celery = make_celery(app)

# route() decorator is used to define the URL where index() function is registered for
@app.route('/')
def index():
	return render_template('index.html')

# event handler for connection where the client recieves a confirmation message upon the connection to the socket 
@socketio.on('connection', namespace='/test')
def confirmation_message(message):
	emit('confirmation', {'connection_confirmation': message['connection_confirmation']})

# event handler for name submission by the client 
@socketio.on('submit_name', namespace='/test')
def name_handler(message):
	session_id = request.sid
	roomstr = session_id
	join_room(roomstr)
	name = message['name']
	message_to_client.delay(name, roomstr)

# message_to_client() function is meant to run as background tasks, so it needs to be decorated with the celery.task decorator 
@celery.task(name="task.message")
def message_to_client(name, room):
	socketio = SocketIO(message_queue='amqp://')
	count = 5
	while count > 1 :
		count -= 1
		socketio.emit('response', {'count': count}, namespace='/test', room=room)
		time.sleep(1)
	socketio.emit('response', {'name': name}, namespace='/test', room=room)



if __name__ == "__main__":
	socketio.run(app, debug=True)


	