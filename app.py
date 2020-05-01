from flask import Flask, render_template, request, jsonify
import json
import pandas as pd
from flask import Response
import os
from surprise import Dataset
from surprise import Reader
from surprise import KNNBasic
from surprise.model_selection import train_test_split
from surprise import dump

# Path to dump file and name
dumpfile = os.path.join('./data/dump/dump_knn_pearsonbaseline_500dump_file')
beer_pickel_path = os.path.join('./data/dump/beer.pkl')

# Load dump files
predictions,algo = dump.load(dumpfile)
beers_df = pd.read_pickle(beer_pickel_path)

# Create the trainset from the algo
trainset = algo.trainset

def get_beer_name (beer_raw_id):
    beer_name = beers_df.loc[beers_df.beer_id==beer_raw_id,'name'].values[0]
    return beer_name

def get_beer_raw_id (beer_name):
    beer_raw_id = beers_df.loc[beers_df.name==beer_name,'beer_id'].values[0]
    return beer_raw_id

def get_beer_style (beer_raw_id):
    beer_style = beers_df.loc[beers_df.beer_id==beer_raw_id,'style'].values[0]
    return beer_style

def get_beer_score_mean (beer_raw_id):
    score_mean = beers_df.loc[beers_df.beer_id==beer_raw_id,'score'].values[0]
    return score_mean

def get_beer_neighbors (beer_raw_id):
    beer_inner_id = algo.trainset.to_inner_iid(beer_raw_id)
    beer_neighbors = algo.get_neighbors(beer_inner_id, k=10)
    beer_neighbors = (algo.trainset.to_raw_iid(inner_id)
                  for inner_id in beer_neighbors)
    return(beer_neighbors)

def get_beer_recc_df (beer_raw_id):
    beer_inner_id = algo.trainset.to_inner_iid(beer_raw_id)
    beer_neighbors = algo.get_neighbors(beer_inner_id, k=10)
    beer_neighbors = (algo.trainset.to_raw_iid(inner_id)
                      for inner_id in beer_neighbors)
    beers_id_recc = []
    beer_name_recc =[]
    beer_style_recc = []
    beer_score_mean = []
    for beer in beer_neighbors:
        beers_id_recc.append(beer)
        beer_name_recc.append(get_beer_name(beer))
        beer_style_recc.append(get_beer_style(beer))
        beer_score_mean.append(get_beer_score_mean(beer))
    beer_reccomendations_df = pd.DataFrame(list(zip(beers_id_recc,beer_name_recc,beer_style_recc,beer_score_mean)),
                                       columns=['beer_id', 'name', 'style', 'score_mean'])
    return beer_reccomendations_df

################################################################
#               Flask Setup                                    #
################################################################
app = Flask(__name__)

################################################################
#                        Flask Routes                          #
################################################################


# --------------------------------------------------------------#
#                       recommender model routes                #
# --------------------------------------------------------------#

@app.route("/") 
def status():
    return "Ready!"

@app.route("/test.html")
def recommender_selector():
    beers = beers_df['name'].tolist()
    return render_template("test.html", beers = beers)

@app.route("/recommendations/<beer_name>")
def nearest_neighbors(beer_name):
    beer_raw_id = get_beer_raw_id(beer_name)
    df = get_beer_recc_df (beer_raw_id)

    # return json of the dataframe
    return Response(df.to_json(orient = "records"), mimetype='application/json')

################################################################
#                           Main                               #
################################################################
if __name__ == "__main__":
    app.run(debug=True)