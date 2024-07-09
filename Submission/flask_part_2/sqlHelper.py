# Import Dependencies
import pandas as pd
import numpy as np
import datetime 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text, func

# This Class is to separate out any Database logic
class SQLHelper():
    #################################################
    # Database Setup
    #################################################

    # Define properties
    def __init__(self):
        self.engine = create_engine("sqlite:///hawaii.sqlite")
        self.Base = None

        # automap Base classes
        self.init_base()

    def init_base(self):
        # reflect an existing database into a new model
        self.Base = automap_base()
        # reflect the tables
        self.Base.prepare(autoload_with=self.engine)

    #################################################
    # Database Queries
    #################################################

    def query_precipitation_orm(self):
        # Save reference to the table
        Measurement = self.Base.classes.measurement

        # Create session (link) from Python to the DB
        session = Session(self.engine)

        # Query the last 12 months of precipitation data.
        # Calculate the date one year from the last date in data set.
        start_date = datetime.date(2016, 8, 23)

        # Perform a query to retrieve the data and precipitation scores
        results = session.query(Measurement.date, Measurement.station, Measurement.prcp).\
            filter(Measurement.date >= start_date).\
            order_by(Measurement.date.asc()).\
            all()

        # Save the query results as a Pandas DataFrame. Explicitly set the column names
        prcp_df = pd.DataFrame(results, columns=["Date", "Station", "Precipitation"])

        # Sort the dataframe by date
        prcp_df["Date"] = pd.to_datetime(prcp_df['Date'])
        prcp_df = prcp_df.sort_values(by="Date", ascending=True).reset_index(drop=True)

        # Close session
        session.close()

        # Create dictionary 
        data = prcp_df.to_dict(orient="records")
        return(data)

    def query_stations_orm(self):
        # Save reference to the table
        Measurement = self.Base.classes.measurement
        Station = self.Base.classes.station

        # Create session (link) from Python to the DB
        session = Session(self.engine)

        # List the stations and their counts in descending order.
        results = session.query(Measurement.station, func.count(Measurement.date)).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.date).desc()).\
            all()

        # Save the query results as a Pandas DataFrame. Explicitly set the column names
        station_df = pd.DataFrame(results, columns=["Station", "Observations"])
        station_df.head()

        # Close session
        session.close()

        # Create dictionary 
        data = station_df.to_dict(orient="records")
        return(data)

    def query_tobs_orm(self):
        # Save reference to the table
        Measurement = self.Base.classes.measurement
        Station = self.Base.classes.station

        # Create session (link) from Python to the DB
        session = Session(self.engine)

        # Query the last 12 months of temp observ data for the most active station.
        # Calculate the date one year from the last date in data set.
        start_date = datetime.date(2016, 8, 23)

        # Perform a query to retrieve the data and tobs scores
        results = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.station == 'USC00519281').\
            order_by(Measurement.date.asc()).\
            all()

        # Save the query results as a Pandas DataFrame. Explicitly set the column names
        most_active_station_df = pd.DataFrame(results, columns=["Date", "Station", "TOBS"])

        # Sort the dataframe by date
        most_active_station_df["Date"] = pd.to_datetime(most_active_station_df['Date'])
        most_active_station_df = most_active_station_df.sort_values(by="Date", ascending=True).reset_index(drop=True)

        # Close session
        session.close()

        # Create dictionary 
        data = most_active_station_df.to_dict(orient="records")
        return(data)

    def query_tobs_start_orm(self, start):
        # Save reference to the table
        Measurement = self.Base.classes.measurement

        # Create session (link) from Python to the DB
        session = Session(self.engine)

        # Query TMIN, TAVG, and TMAX for a specified start.
        # Calculate TMIN, TAVG, and TMAX for all dates >= start date.
        start_date = datetime.datetime.strptime(start, '%Y-%m-%d')

        # Perform a query to retrieve the data and tobs scores
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).\
            all()

        # Save the query results as a Pandas DataFrame. Explicitly set the column names
        tobs_start_df = pd.DataFrame(results, columns=["min_tobs", "avg_tobs", "max_tobs"])

        # Close session
        session.close()

        # Create distionary
        data = tobs_start_df.to_dict(orient="records")
        return(data)

    def query_tobs_start_end_orm(self, start, end):
        # Save reference to the table
        Measurement = self.Base.classes.measurement

        # Create session (link) from Python to the DB
        session = Session(self.engine)

        # Query TMIN, TAVG, and TMAX for start-end range.
        # Calculate TMIN, TAVG, and TMAX for start-end range.
        start_date = datetime.datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end, '%Y-%m-%d')

        # Perform a query to retrieve the data and tobs scores
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).\
            all()

        # Save the query results as a Pandas DataFrame. Explicitly set the column names
        tobs_start_end_df = pd.DataFrame(results, columns=["min_tobs", "avg_tobs", "max_tobs"])

        # Close session
        session.close()

        # Create dictionary 
        data = tobs_start_end_df.to_dict(orient="records")
        return(data)
