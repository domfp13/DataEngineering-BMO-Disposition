#!/usr/bin/env python
# Luis Enrique Fuentes Plata
# To test locally 
# docker container run -d --name bmo -p 9090:8080 -e PORT=8080 -e GOOGLE_SHEET="BMO_Disposition_2020.xlsx" -e BUCKET_NAME="appusma206_apps_output" -e GOOGLE_APPLICATION_CREDENTIALS="/app/Keys/creds.json" img_bmo

import logging
from flask import Flask
from os.path import basename
from os import environ
from resources.GenericFunctions import (getWorkBook, getBucket, upload_blob)
from resources.GoogleSheets import SpreadSheet
from resources.DataAnalysis import DataFrames
from resources.GenericClasses import Time
from json import dumps

app = Flask(__name__)

@app.route('/')
def index():

    try:

        logging.info("--Begin--")

        # Getting enviromental variables
        logging.info("1.- Loading env variables")
        GOOGLE_SHEET_WORKBOOK = getWorkBook()
        BUCKET_NAME = getBucket()

        # Setting up objects
        logging.info("2.- Setting up objs - spreadSheet, dataframes, time")
        spreadSheet = SpreadSheet(GOOGLE_SHEET_WORKBOOK)
        dataframes = DataFrames()
        time = Time()

        # List that will hold the months that has to be process (jan, feb, etc)
        logging.info("3.- Adding month(s) to process")
        months_to_process = []
                # Checking if last month is needed: the rule of 7 days and if the year of the previus month is the same from current one
        if time.getCurrentDay() in range(1,8) and time.getCurrentYear() == time.getLastdayLastmonth().year:
            months_to_process.append(time.getCurrentMonthStr()[0:3].lower())
            months_to_process.append(time.getLastMonthStr()[0:3].lower())
        else:
            months_to_process.append(time.getCurrentMonthStr()[0:3].lower())

        # @Testing
        # del months_to_process
        # months_to_process = ['jan','feb','mar']
        # @Testing

        # Start processing the months
        logging.info("4.- Processing months")
        counter = 0
        for month in months_to_process:
            for sheet in spreadSheet.getAllSheets():
                if month in sheet.strip().lower():
                    # Gets data from Google sheets and put it into a local file
                    logging.info(f"  Processing: {month}")

                    spreadSheet.addSheet(sheet)
                    dataframes.addDataFrame(spreadSheet.sheets[counter], sheet_name=month, year=time.getCurrentYear(), month=time.getMonthByString(month))

                    counter = counter + 1

        logging.info("5.- Merging Data")
        dataframes.mergeDataFrames()

        logging.info("6.- Transforming to CSV")
        file_full_path = dataframes.convertToCSV()

        logging.info("7.- Uploading to bucket")
        upload_blob(BUCKET_NAME, file_full_path, f'appusma206_apps/BMO_Disposition/{basename(file_full_path)}')

        return dumps({'success': True}), 200, {'ContentType': 'application/json'}
    
    except Exception as e:
        logging.exception(e)
        return dumps({'success': False}), 400, {'ContentType': 'application/json'}

if __name__== '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(environ.get('PORT', 8080)))