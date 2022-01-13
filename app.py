from flask import Flask, redirect, render_template
from pymongo import MongoClient

import pandas as pd
import numpy as np
from plots import *
import json
import matplotlib.pyplot as plt
import statistics
import csv
from optparse import OptionParser
import redis
import sys

app =  Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/refresh_plots', methods=['GET'])
def refresh_plots():

   
    
    #get and mutate dataframe 
    with open('yearsdata.json') as json_file:
        yearsdata = json.load(json_file)
    with open('countriesdata.json') as json_file2:
        countriesdata = json.load(json_file2)
    # df = df.set_index('Reference Area')
    # del df['_id']
    # df['Time Period'] = pd.to_numeric(df['Time Period'])
    # df['Observation Value'] = pd.to_numeric(df['Observation Value'])
    # df = df.sort_values('Observation Value')
    # print(df)
    count = 0
    for country, payload in countriesdata.items():
    
        plt.title(country)
        plt.ylabel("Female to male population ratio")
        plt.xlabel("Years")
        years =[] 
        datas = []
        for year, data in payload.items(): 
            if year == "Country Code" or year == "Color":
                break
            years.append(year)
            counterdata = 100 - data
            datas.append(data/counterdata)
        x = np.array(years)
        y = np.array(datas)
        plt.bar(x,y, color = countriesdata[country]["Color"])
        plt.savefig('./static/images/hbars3_{count}.png')
        plt.show()
        count+=1
    
    # #generate plots
    # bar_plots(df)
    # dispersion_plots(df)
    # box_plots(df)

    return redirect("/")





#!/usr/bin/env python
'''
:mod:`csv2redis.csv2redis` is a module containing classes for importing CSV files to Redis.
'''




def import_csv(key_col=1, csv_file="yearsdata.csv", redis_host='egbadon.redis.cache.windows.net', redis_port=6379, azurePassword='HHDI4wBkIcTgmCSvZD0nxgxaPvZw2iYEtAzCaG9897c='):
    pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=0, password=azurePassword)
    r = redis.Redis(connection_pool=pool)
    pipe = r.pipeline()
    with open(csv_file, 'r') as cf:
        cfreader = csv.reader(cf)
        headers = cfreader.__next__()
        for row in cfreader:
            record = {}
            for h, v in zip(headers, row):
                record[h] = v
            pipe.hmset(row[key_col], record)
    pipe.execute()


if __name__ == "__main__":
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-f", "--file", dest="csvfile", help="CSV file to import", metavar="FILE")
    parser.add_option("-n", "--name-column", dest="namecolumn", help="Column number to use as name")
    parser.add_option("-r", "--redis-host", dest="redishost", help="Redis host name", default="localhost")
    parser.add_option("-p", "--redis-port", dest="redisport", help="Redis port", default=6379)

    (options, args) = parser.parse_args()

    # if options.csvfile is None:
    #     parser.error("Missing reqiured option csv file")
    #
    # if options.namecolumn is None:
    #     parser.error("Missing required option name column")

    # import_csv(int(options.namecolumn), options.csvfile, options.redishost, options.redisport)
    import_csv()



if __name__ == "__main__":
    app.run(debug=True)