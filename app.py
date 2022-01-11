from flask import Flask, redirect, render_template
from pymongo import MongoClient

import pandas as pd
import numpy as np
from plots import *

app =  Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/refresh_plots', methods=['GET'])
def refresh_plots():

    #connect to db
    CONNECTION_STRING = "mongodb+srv://owolabioromidayo:thisisdayo99@cluster0.28vgr.mongodb.net/gdp_country?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    collection = client['gdp_country']['gdp_country']
    cursor = collection.find()
    
    #get and mutate dataframe 
    df = pd.DataFrame(list(cursor))
    df = df.set_index('Reference Area')
    del df['_id']
    df['Time Period'] = pd.to_numeric(df['Time Period'])
    df['Observation Value'] = pd.to_numeric(df['Observation Value'])
    df = df.sort_values('Observation Value')
    print(df)
    
    #generate plots
    bar_plots(df)
    dispersion_plots(df)
    box_plots(df)

    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)