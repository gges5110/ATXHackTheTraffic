#!/usr/bin/python
# -*- coding: ascii -*-

from flask import Flask, render_template, jsonify, url_for, request, redirect
import os, util

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
import database_init

# Routing setup
from views.index import index
from views.problemStatement import problemStatement
from views.travelTimePrediction import travelTimePrediction
from views.historyStats import historyStats
from views.heatmap import heatmap
from views.about import aboutUs

app = Flask(__name__)
app.register_blueprint(index)
app.register_blueprint(problemStatement)
app.register_blueprint(travelTimePrediction)
app.register_blueprint(historyStats)
app.register_blueprint(heatmap)
app.register_blueprint(aboutUs)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    port = int(os.environ.get("PORT", 8000))
    app.run(host = '0.0.0.0', port = port)
