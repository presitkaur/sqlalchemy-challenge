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

# Save references to each table
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

#Route for stations page 
@app.route("/api/stations")
def stations():
    station_data = session.query(station).all()

    stations_list = []
    for station in station_data:
        station_dict = {}
        station_dict["id"] = station.id
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        station_dict["latitude"] = station.latitude
        station_dict["longitude"] = station.longitude
        station_dict["elevation"] = station.elevation
        stations_list.append(station_dict)

    return jsonify(stations_list)

#Route for monthly temperature oberservations page 
@app.route("/api/tobs")
def monthly_temp():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    result = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= prev_year).all()
    tobs = list(np.ravel(result))
    return jsonify(tobs=tobs)

#Route for start and start/end pages 
@app.route("/api/<start>")
def start(start=None):
    start = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).group_by(measurement.date).all()
    start_list=list(start)
    return jsonify(start_list)

@app.route("/api/temp/<start>/<end>")
def start_end(start=None, end=None):
    between_dates = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).group_by(measurement.date).all()
    between_dates_list=list(between_dates)
    return jsonify(between_dates_list)

if __name__ == '__main__':
    app.run()
