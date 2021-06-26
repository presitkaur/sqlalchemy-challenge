#Import dependencies 
import pandas as pd
import numpy as np 
import sqlalchemy
from sqlalchemy import create_engine, func, MetaData, Table, Column, ForeignKey
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
from flask import Flask, jsonify 

#Set up Flask

app = Flask(__name__)

#Create engine
engine = create_engine("sqlite:///hawaii.sqlite")

#Create a new model for the database
base = automap_base()
base.prepare(engine, reflect=True)

# # Save references to each table
measurement = base.classes.measurement
station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#Create a home page route
@app.route("/")
def home():
    return(
        f"The following are all the available routes: <br/>"
        f"/api/precipitation<br/>"
        f"/api/stations<br/>"
        f"/api/tobs<br/>"
        f"/api/temp/<start><br/>"
        f"/api/temp/<start>/<end>"

    )
    
#Route for the precipitation page 
@app.route("/api/precipitation")
def precip():
    year = dt.date(2017,8,23) - dt.timedelta(days=365)
    result = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year).all()
    precipitation = {date: prcp for date, prcp in result}
    return jsonify(precipitation)

@app.route("/api/stations")
def stations():
    """Return a list of stations."""
    results = session.query(station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)


@app.route("/api/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


@app.route("/api/temp/<start>")
@app.route("/api/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


if __name__ == '__main__':
    app.run()
