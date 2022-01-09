import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# # REF Return the table names
# Base.classes.keys()

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return (
        f"Welcome to Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Min, Mean, Max temperature statistics data starting by date entered<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>"
        f"Min, Mean, Max temperature statistics data for range between dates entered<br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD<br/>"
    )


# #Convert the query results to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all date and prcp"""
    # Query
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_prcp = []
    for date, prcp in results:
        dates_dict = {}
        dates_dict["date"] = date
        dates_dict["prcp"] = prcp
        all_prcp.append(dates_dict)

    return jsonify(all_prcp)

# #Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


# # Query the dates and temperature observations of the most active station for the last year of data.
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.date > "2016-08-18").filter(Measurement.station == "USC00519281").all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    active_tobs = []
    for station, date, tobs in results:
        dates_dict = {}
        dates_dict["station"] = station
        dates_dict["date"] = date
        dates_dict["tobs"] = tobs
        active_tobs.append(dates_dict)

    return jsonify(active_tobs)

# # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

# # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date > start).all()

    # Convert list of tuples into normal list
    start_stats = list(np.ravel(result))

    return jsonify(start_stats)


# # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date < end).filter(Measurement.date > start).all()

    # Convert list of tuples into normal list
    start_stats = list(np.ravel(result))

    return jsonify(start_stats)


if __name__ == "__main__":
    app.run(debug=True)