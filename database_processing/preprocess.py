import pandas as pd
import time as t
import sys
import csv, sqlite3
import os.path
import numpy as np

# Return a dataframe with Origin, Destination, Time, Weekday, Year, Samples
# and Average time*Sample, total of 7 columns
def getTimeWeekdayYear(df):
    weekday = []  # range [0, 6], Monday is 0
    year = []
    time = [] # from 0 - 2399
    ts = df.timestamp
    row_count = 0
    for row in ts.values:
        # dt = datetime.datetime.strptime(row, '%m/%d/%Y %I:%M:%S %p')
        # time.append(datetime.datetime.strftime(dt, '%H:%M'))

        strip_time = t.strptime(row, '%m/%d/%Y %I:%M:%S %p')
        hour = strip_time.tm_hour
        minute = strip_time.tm_min
        time.extend([hour*60+minute])
        weekday.extend([strip_time.tm_wday])
        year.extend([strip_time.tm_year])

        row_count += 1
        if row_count % 100000 == 0:
            print "Processing row " + str(row_count)

    print "Total row count: " + str(row_count) + ' rows\n'

    avg_time_mul_sample = df.average_travel_time_seconds * df.number_samples

    df2 = pd.DataFrame({"Origin": df.origin_reader_identifier, "Destination": df.destination_reader_identifier,
                        'Time': time, 'Year': year, 'Weekday': weekday,
                        'Samples': df.number_samples, "time_mul_sample": avg_time_mul_sample})
    return df2


# Calculate the weighted average travel time column and add Time, Weekday, and Year column
def preprocess(df):
    df2 = getTimeWeekdayYear(df)

    aggregations = {
        'time_mul_sample': {
            'sum_time_mul_sample': 'sum'
        },
        'Samples': {
            'total_sample': 'sum'
        }

    }
    df3 = df2.groupby(['Origin', 'Destination', 'Year', 'Weekday', 'Time']).agg(aggregations).reset_index()
    df3.columns = ['Origin', 'Destination', 'Year', 'Weekday', 'Time', "Total_sample", "sum_time_mul_sample"]

    avg_travel_time = df3.sum_time_mul_sample/df3.Total_sample

    df4 = pd.DataFrame({"Origin": df3.Origin, "Destination": df3.Destination,
                        'Year': df3.Year, 'Weekday': df3.Weekday, 'Time': df3.Time,
                        'Avg_travel_time': avg_travel_time.apply(int)})
    return df4

if __name__ == "__main__":
    # start_time = t.time()
    # Process Travel_Sensors.csv
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    #TODO make a promt here to confirm if user really wants to create a new table.

    # Drop table if the table exists
    drop_travel_sensor_table_query = "DROP TABLE IF EXISTS TravelSensor"
    cur.execute(drop_travel_sensor_table_query)

    create_travel_sensor_table_query = "              \
        CREATE TABLE IF NOT EXISTS TravelSensor(\
        ID          INT PRIMARY KEY NOT NULL,   \
        READER_ID   TEXT            NOT NULL,   \
        LATITUDE    REAL            NOT NULL,   \
        LONGITUDE   REAL            NOT NULL    \
        )                                       \
    "
    cur.execute(create_travel_sensor_table_query)

    travel_sensors_csv = "/../Travel_Sensors.csv"
    with open(os.path.dirname(__file__) + travel_sensors_csv,'rb') as fin: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        data_row = csv.DictReader(fin) # comma is default delimiter
        to_db = [(i['ATD_SENSOR_ID'], i['READER_ID'], i['LATITUDE'], i['LONGITUDE']) for i in data_row]

    cur.executemany("INSERT INTO TravelSensor (ID, READER_ID, LATITUDE, LONGITUDE) VALUES (?, ?, ?, ?);", to_db)
    con.commit()

    drop_summary_table_query = "DROP TABLE IF EXISTS Summary"
    cur.execute(drop_summary_table_query)

    create_summary_table_query = "          \
        CREATE TABLE IF NOT EXISTS Summary( \
        Id INT PRIMARY KEY NOT NULL,        \
        Avg_Travel_Time REAL NOT NULL,      \
        Destination TEXT NOT NULL,          \
        Origin TEXT NOT NULL,               \
        Time INT NOT NULL,                  \
        Weekday INT NOT NULL,               \
        Year INT NOT NULL                   \
        )                                   \
    "
    cur.execute(create_summary_table_query)

    summary_csv = "/../preprocessed_summary.csv"
    if not os.path.isfile(os.path.dirname(__file__) + summary_csv) :
        print "Cannot find preprocessed_summary.csv, creating a new one from TMSR..."
        # Download .csv file from https://data.austintexas.gov/dataset/Travel-Sensors-Match-Summary-Records/v7zg-5jg9/data
        TMSR_csv = "/../Bluetooth_Travel_Sensors_-Traffic_Match_Summary_Records__TMSR_.csv"

        df = pd.read_csv(os.path.dirname(__file__) + TMSR_csv, dtype={
            'timestamp': np.object,
            'average_travel_time_seconds': np.int64,
            'number_samples': np.int64,
            'origin_reader_identifier': np.object,
            'destination_reader_identifier': np.object
            })

        df4 = preprocess(df)
        df4.to_csv(os.path.dirname(__file__) + summary_csv, index=True, index_label="index")
        print "Finished preprocessing data!"

    with open(os.path.dirname(__file__) + summary_csv,'rb') as fin: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        data_row = csv.DictReader(fin) # comma is default delimiter
        # TODO use number index instead of string in i[]
        to_db = [(i['index'], i['Avg_travel_time'], i['Destination'], i['Origin'], i['Time'], i['Weekday'], i['Year']) for i in data_row]

    cur.executemany("INSERT INTO Summary (Id, Avg_Travel_Time, Destination, Origin, Time, Weekday, Year) VALUES (?, ?, ?, ?, ?, ?, ?);", to_db)
    con.commit()

    con.close()

    # Column names and data types for Bluetooth_Travel_Sensors_-Traffic_Match_Summary_Records__TMSR.csv
    # record_id                         object
    # origin_reader_identifier          object
    # destination_reader_identifier     object
    # origin_roadway                    object
    # origin_cross_street               object
    # origin_direction                  object
    # destination_roadway               object
    # destination_cross_street          object
    # destination_direction             object
    # segment_length_miles             float64
    # timestamp                         object
    # average_travel_time_seconds        int64
    # average_speed_mph                  int64
    # summary_interval_minutes           int64
    # number_samples                     int64
    # standard_deviation               float64
