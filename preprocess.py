import pandas as pd
import time as t
import sys
from sqlalchemy import create_engine

engine = create_engine('sqlite:///summary.db', echo=True)

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
                        'Avg_travel_time': avg_travel_time.apply(int), 'Sample_count': df3.Total_sample})
    return df4

if __name__ == "__main__":
    start_time = t.time()

    # Download .csv file from https://data.austintexas.gov/dataset/Travel-Sensors-Match-Summary-Records/v7zg-5jg9/data
    path = sys.argv[1]
    df = pd.read_csv(path)

    df4 = preprocess(df)
    # df4.to_csv('preprocessed_summary.csv', index=False)
    df4.to_sql('Summary', index=True, con=engine)
    # print df4
    print "Finished preprocessing data!"

    duration = t.time() - start_time
    print "Total run time = " + str(duration) + "s\n"


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

