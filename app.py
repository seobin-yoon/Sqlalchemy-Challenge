#################################################
# Dependencies
#################################################
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# View all of the classes that automap found
Base.classes.keys()
# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    # List all available api routes
    return(
        f"Available Routes: <br>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():

    Session = Session(engine)
    Precipitations = Session.query(Measurement.date, Measurement.prcp).all()
    
    Session.close()

    PrcpList = []
    for date, prcp in Precipitations:
        PrcpDict = {}
        PrcpDict['date'] = date
        PrcpDict['prcp'] = prcp
        PrcpList.append(PrcpDict)

    return jsonify(PrcpList)



@app.route("/api/v1.0/stations")
def stations():

    Session = Session(engine)
    Stations = Session.query(Station.station).distinct().all()
    
    Session.close()

    StnList = []
    for station in Stations:
        StnDict = {}
        StnDict['station'] = station
        StnList.append(StnDict)

    return jsonify(StnList)



@app.route("/api/v1.0/tobs")
def tobs():

    Session = Session(engine)

    Recent_date = Session.query(Measurement).order_by(Measurement.date.desc()).first()
    Query_date = dt.datetime.strptime(Recent_date.date, '%Y-%m-%d').date() - dt.timedelta(days=365)
    
    Active_stations = Session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()

  
    Active_st = 'USC00519281'
    station_temp = Session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), 
                             func.avg(Measurement.tobs)).filter(Measurement.station == Active_st).all()
    
    Session.close()

    TobList = []
    for date, temp in station_temp:
        TempDict = {}
        TempDict['date'] = date
        TempDict['temperature'] = temp
        TobList.append(TempDict)

    return jsonify(TobList)



@app.route("/api/v1.0/<start>")
def start_date(start):

    Session = Session(engine)
   
    StartDate = Session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    Session.close
    DateList = []
    for date in StartDate:
        DateDict = {}
        DateDict['Start'] = date
        DateDict['Min Temp'] = date[0]
        DateDict['Max Temp'] = date[1]
        DateDict['Avg Temp'] = date[2]
        DateList.append(DateDict)

    return jsonify(DateList)



@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    Session = Session(engine)

    start_end_dates = Session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()
    Session.close
    StartEndList = []
    for date in start_end_dates:
        StartEndDict = {}
        StartEndDict['Start'] = start
        StartEndDict['End'] = end
        StartEndDict['Min Temp'] = date[0]
        StartEndDict['Max Temp'] = date[1]
        StartEndDict['Avg Temp'] = date[2]
        StartEndList.append(StartEndDict)

    return jsonify(StartEndList) 


if __name__ == '__main__':
    app.run(debug=True)