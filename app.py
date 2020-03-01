import os

import pandas as pd
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/bellybutton.sqlite"
db = SQLAlchemy(app)

Base = automap_base()

Base.prepare(db.engine, reflect=True)

Samples_Metadata = Base.classes.sample_metadata
Samples = Base.classes.samples


@app.route("/")
def index():
   
    return render_template("index.html")


@app.route("/names")
def names():
      
    statement = db.session.query(Samples).statement
    df = pd.read_sql_query(statement, db.session.bind)

  
    return jsonify(list(df.columns)[2:])


@app.route("/metadata/<sample>")
def sample_metadata(sample):

    results = db.session.query(Samples_Metadata.sample, Samples_Metadata.ETHNICITY,
        Samples_Metadata.GENDER,
        Samples_Metadata.AGE,
        Samples_Metadata.LOCATION,
        Samples_Metadata.BBTYPE,
        Samples_Metadata.WFREQ).filter(Samples_Metadata.sample == sample).all()

 
    sample_meta = {}
    for result in results:
        sample_meta["sample"] = result[0]
        sample_meta["ETHNICITY"] = result[1]
        sample_meta["GENDER"] = result[2]
        sample_meta["AGE"] = result[3]
        sample_meta["LOCATION"] = result[4]
        sample_meta["BBTYPE"] = result[5]
        sample_meta["WFREQ"] = result[6]

  
    return jsonify(sample_meta)


@app.route("/samples/<sample>")
def samples(sample):
    
    statement = db.session.query(Samples).statement
    df = pd.read_sql_query(statement, db.session.bind)


    selected_data = df.loc[df[sample] > 5, ["otu_id", "otu_label", sample]]

   
    selected_data.sort_values(by=sample, ascending=False, inplace=True)

   
    data = {
        "otu_ids": selected_data.otu_id.values.tolist(),
        "sample_values": selected_data[sample].values.tolist(),
        "otu_labels": selected_data.otu_label.tolist(),
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
