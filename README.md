
# Flask-SocketIO integration with Celery
This repository contains an example code which shows the integration between Flask, Socket.IO and Celery. The application is made in Flask where a counting task, representing a lengthy task, is performed by the celery worker. To update the client with the status of the task, Flask-SocketIO (by Miguel Grinberg) is used in the application to communicate with the celery task and report to the client. 

## Quick Setup
1. Clone this repository.  
2. Create a virtualenv.  
3. Install the requirements:`$ pip install -r requirements.txt`.  
4. Open a second terminal window and start a local RabbitMQ server: `$ rabbitmq-server`.  
5. Open a third terminal window and starta Celery worker: `$ venv/bin/celery worker -A app.celery --loglevel=info`.
6. Start the Flask application on your original terminal window:`$ venv/bin/python app.py`.  
7. Finally, go to `http://localhost:5000/`.  

Hope it is helpful!
