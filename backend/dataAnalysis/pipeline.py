import tempAPI
import lstRead
import predictiveModel
import sys

def pipeline(longitude, latitude, region, startDate, endDate):
    tempAPI.fetch_data(longitude, latitude, region, startDate, endDate)
    lstRead.format_data()
    predictiveModel.predict()