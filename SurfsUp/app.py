# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import datetime as dt

#################################################
# Database Setup
#################################################
# print('the app is alive and it took zero effort unlike on fucking windows')
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Homepage endpoint
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        "HAWAII API<br>"
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end>"
    )

# precip endpoint
@app.route("/api/v1.0/precipitation")
def precip():
    print("Server received request for 'precipitation' page...")
    
    # define last year of precipitation data
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d').date()
    query_date = latest_date - dt.timedelta(days=365)

    # run query based on last year of precipitation data
    query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()

    # make dictionary
    precipitation_dict = {}
    for date, prcp in query:
        precipitation_dict[date] = prcp

    # return dictionary JSONified    
    return jsonify(precipitation_dict)

    session.close()

# stations endpoint (3. Return a JSON list of stations from the dataset)
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")
    
    sel = [Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation]
    query = session.query(*sel).all()

    stations = []
    for station,name,lat,lng,el in query:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lng"] = lng
        station_dict["Elevation"] = el
        stations.append(station_dict)

    return jsonify(stations)

# 4. Query the dates and temperature observations of the most-active station for the previous year of data.
    # Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():

    # define last year of precipitation data
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d').date()
    query_date = latest_date - dt.timedelta(days=365)

    sel = [Measurement.date,Measurement.tobs]
    query = session.query(*sel).filter(Measurement.date >= query_date).all()
    
    tobsall = []
    for date, tobs in query:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobsall.append(tobs_dict)

    return jsonify(tobsall)

    

# ///
if __name__ == "__main__":
    app.run(debug=True)

print('''
      // The End //
      ''')
