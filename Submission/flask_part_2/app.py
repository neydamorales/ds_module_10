# Import Dependencies
from flask import Flask, jsonify
import pandas as pd
import numpy as np
import datetime as dt
from sqlHelper import SQLHelper

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
sql = SQLHelper()

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation_orm<br/>"
        f"/api/v1.0/stations_orm<br/>"
        f"/api/v1.0/tobs_orm<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"<p>'start' and 'end' date should be in the format YYYY-MM-DD.</p>"
    )

# SQL Queries
@app.route("/api/v1.0/precipitation_orm")
def precipitation_orm():
    data = sql.query_precipitation_orm()
    return(jsonify(data))

@app.route("/api/v1.0/stations_orm")
def stations_orm():
    data = sql.query_stations_orm()
    return(jsonify(data))

@app.route("/api/v1.0/tobs_orm")
def tobs_orm():
    data = sql.query_tobs_orm()
    return(jsonify(data))

# replace <start> with format 2016-08-23 in URL
@app.route("/api/v1.0/<start>")
def tobs_start_orm(start):
    data = sql.query_tobs_start_orm(start)
    return(jsonify(data))

# replace <start> with 2016-08-23 / <end> with 2017-08-23 in URL
@app.route("/api/v1.0/<start>/<end>")
def tobs_start_end_orm(start, end):
    data = sql.query_tobs_start_end_orm(start, end)
    return(jsonify(data))

# Run the App
if __name__ == '__main__':
    app.run(debug=True)
