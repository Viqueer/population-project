from flask import Flask, redirect, render_template
from pymongo import MongoClient

import pandas as pd
import numpy as np
from plots import *
import json
import matplotlib.pyplot as plt
import statistics

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



if __name__ == "__main__":
    app.run(debug=True)