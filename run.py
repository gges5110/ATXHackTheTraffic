#!/usr/bin/python
# -*- coding: ascii -*-

from flask import Flask, render_template, jsonify, url_for, request, redirect
import os, util

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, TravelSensor

engine = create_engine('sqlite:///database1.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Routing setup
from views.route1 import route1
from views.route2 import route2
from views.route3 import route3
app = Flask(__name__)
app.register_blueprint(route1)
app.register_blueprint(route2)
app.register_blueprint(route3)

@app.route('/', methods=['GET'])
def index():
    user = session.query(User).first()
    return_from_util = util.example_function()
    return render_template('index.html', user=user, msg=return_from_util)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    port = int(os.environ.get("PORT", 8000))
    app.run(host = '0.0.0.0', port = port)
