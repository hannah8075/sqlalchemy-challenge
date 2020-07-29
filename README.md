# sqlalchemy-challenge
The climate analysis jupyter notebook contains basic climate analysis and data exploration using python and SQLAlchemy. The analysis found:
- precipitation over time and summary statistics of precipitation data
- total number of stations and most active stations
- t-test of June vs Dec temperatures
- average temp for a defined date range
- daily rainfall average

The app.py provides a Flask API with the following routes:
- /api/v1.0/precipitation
- /api/v1.0/stations
- /api/v1.0/tobs
- /api/v1.0/<start>
- /api/v1.0/<start>/<end>
