# import dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
from flask import Flask, jsonify
import numpy as np
import datetime as dt

# database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

# flask setup
app = Flask(__name__)

# set date variables
last_date = dt.date(2017, 8 ,23)
date_12mos_ago = last_date - dt.timedelta(days=365)

# flask routes
# set index/home route
@app.route("/")
def home():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# return JSON of a dictionary using date as the key and prcp as the value
@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)

    sel = [Measurement.date, Measurement.prcp]

    results = session.query(*sel).filter(Measurement.date >= date_12mos_ago).all()
    session.close()

    prcp_dict = {date: prcp for date, prcp in results}
    return jsonify(prcp_dict)

# return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# query the dates and temperature observations of the most active station for the last year of data.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= date_12mos_ago).all()
    session.close()
    temp = [result[0] for result in results]

    return jsonify(temp)

# return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end rangee("/api/v1.0/<start>")
@app.route("/api/v1.0/<start_date>")
def start(start_date):
    session = Session(engine)

    results = (session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date.between(start_date, '2017-08-23')).all())
    tmin = [result[0] for result in results]
    tmax = [result[1] for result in results]
    tavg = [result[2] for result in results]
    return jsonify(tmin,tmax,tavg)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date,end_date):
    session = Session(engine)

    results = (session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date.between(start_date, end_date)).all())
    tmin = [result[0] for result in results]
    tmax = [result[1] for result in results]
    tavg = [result[2] for result in results]
    return jsonify(tmin,tmax,tavg)

if __name__ == "__main__":
    app.run(debug=True)