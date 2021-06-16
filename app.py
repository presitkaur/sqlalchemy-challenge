#Import dependencies 
import pandas as pd
import numpy as np 
import sqlalchemy
from sqlalchemy import create_engine, func
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
        f"/api/temp/start/end"

    )
    
#Route for the precipitation page 
@app.route("/api/precipitation")
def precip():
    year = dt.date(2017,8,23) - dt.timedelta(days=365)
    result = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year).all()
    precip = {date: prcp for date, prcp in result}
    return jsonify(precip)

if __name__ == '__main__':
    app.run()
