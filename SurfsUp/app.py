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
    
    
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d').date()
    query_date = latest_date - dt.timedelta(days=365)
    query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()

    precipitation_dict = {}
    for date, prcp in query:
        precipitation_dict[date] = prcp
        
    return jsonify(precipitation_dict)

    session.close()


# ///
if __name__ == "__main__":
    app.run(debug=True)

print('''
      // The End //
      ''')
