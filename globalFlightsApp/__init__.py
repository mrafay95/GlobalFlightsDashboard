from flask import Flask

app = Flask(__name__)

from globalFlightsApp import routes
