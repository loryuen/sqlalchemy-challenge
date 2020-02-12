########## import dependencies ###########
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

########## set up Database ##########
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Base.classes.keys
Measurement = Base.classes.measurement
Station = Base.classes.station

######## set up Flask ##########
app = Flask(__name__)

####### set up Flask Routes #######

@app.route("/")
def home():
    "List of all available API routes"
    return (
        f'Available Routes:<br/>'
        f'Precipitation: /api/v1.0/precipitation<br/>'
        f'Stations: /api/v1.0/stations<br/>'
        f'Temperature Observations: /api/v1.0/tobs<br/>'
        f'Min, avg and max temps for a given start date (yyyy-mm-dd): /api/v1.0/startdate<br/>'
        f'Min, avg and max temps for a given start and end date (yyyy-mm-dd): /api/v1.0/startdate/enddate'
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session link from python to DB
    session = Session(engine)
    # Query for date and precipitation
    date_prcp = session.query(Measurement.date, Measurement.prcp).all()
    # close session link
    session.close
    
    # Create a dictionary and append to list of all_prcp
    all_prcp = []
    for date, prcp in date_prcp:
        all_prcp_dict = {}
        all_prcp_dict['date'] = date 
        all_prcp_dict['prcp'] = prcp
        all_prcp.append({date:prcp})

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # create session link from python to DB
    session = Session(engine)
    
    # query for stations
    stations = session.query(Station.station).all()

    # close session
    session.close
    
    # create list
    all_stations = list(np.ravel(stations))
    
    # alternate method - dictionary and include station name and id
   # all_stations = []
   # for each, name in stations:
   #     stations_dict = {}
   #     stations_dict['station']=each
   #     stations_dict['name']=name
   #     all_stations.append({each:name})

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # create session link
    session = Session(engine)

    # query for date and temp from a year from the last data point
    date_temp_year = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-23').\
        all()

    # close session
    session.close

    # creat list and return jsonified data 
    yeartemps = []
    for d, t in date_temp_year:
        temp_dict ={}
        temp_dict['date']=d
        temp_dict['tobs']=t
        yeartemps.append({d:t})
        
    return jsonify (yeartemps)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # create session link
    session = Session(engine)

    # query for min, avg and max temps for dates greater than or equal to start date
    startdate = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    # close session
    session.close

    return jsonify(startdate)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # create session link
    session = Session(engine)

    # query for min, avg and max temps for dates greater than or equal to start date
    startenddate = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    # close session
    session.close

    return jsonify(startenddate)

if __name__ == '__main__':
    app.run(debug=True)
