from flask import Flask
from threading import Thread
import random

app = Flask('')

@app.route('/')
def home():
	return "Yep, I'm here!"

def run():
  app.run(
		host='0.0.0.0',
		port=random.randint(2000,9000)
	)

def keep_alive():
	'''
	Creates and starts new thread that runs the function run.
	'''
	t = Thread(target=run)
	t.start()