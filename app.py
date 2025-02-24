from flask import Flask, jsonify
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Create engine to connect to database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)

# Map tables safely
Measurement = Base.classes.get("measurement")
Station = Base.classes.get("station")

# Flask app setup
app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"<center><h2>Welcome to the Hawaii Climate Analysis Local API</h2></center>"
        f"<center><h3>Select from one of the available routes:</h3></center>"
        f"<center>/api/v1.0/precipitation</center>"
        f"<center>/api/v1.0/stations</center>"
        f"<center>/api/v1.0/tobs</center>"
        f"<center>/api/v1.0/start/end</center>"
    )


#/api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precip():
    """Return JSON of precipitation data for the last year"""

    # Calculate the date one year from the last available date
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Create a session inside the route
    session = Session(engine)

    # Query to retrieve the date and preciptation value
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= previous_year).all()

    # Close session
    session.close()

    # Create dictionary {date: precipitation}
    precipitation = {date: prcp for date, prcp in results}

    # Return as JSON
    return jsonify(precipitation)

# /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    
    # Create a session inside the route
    session = Session(engine)
    
    # show a list of stations
    # Query to retrieve name of the stations
    results = session.query(Station.station).all()
    session.close()

    station_list = list(np.ravel(results))

    #convert to a json and display
    return jsonify(station_list)

# /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def temperatures():
    # return the previous year temperatures
     # Calculate the date one year from the last available date
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Create a session inside the route
    session = Session(engine)

    # perform a query to retrieve the temp from most active station from the past year
    results = session.query(Measurement.tobs).\
            filter(Measurement.station == 'USC00519281').\
           filter(Measurement.date >= previous_year).all()
    
    # Close session
    session.close()
    
    temperature_list = list(np.ravel(results))

    #return the list of temperatures
    return jsonify(temperature_list)

# /api/v1.0/start/end
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def date_starts(start=None, end=None):

    # Create a session inside the route
    session = Session(engine)

    #select statement
    selection = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]

    if not end:

        start_date = dt.datetime.strptime(start, "%m%d%Y")

        results = session.query(*selection).filter(Measurement.date >= start_date).all()

        session.close()

        temperature_list = list(np.ravel(results))

        #return the list of temperatures
        return jsonify(temperature_list)
    
    else:
        
        start_date = dt.datetime.strptime(start, "%m%d%Y")
        end_date = dt.datetime.strptime(start, "%m%d%Y")

        results = session.query(*selection)\
            .filter(Measurement.date >= start_date)\
            .filter(Measurement.date <= end_date).all()
            
        session.close()

        temperature_list = list(np.ravel(results))

        #return the list of temperatures
        return jsonify(temperature_list)
    

if __name__ == '__main__':
    app.run(debug=True)
