from flask import Flask, render_template, request, jsonify
import sqlalchemy as sql
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import config
import pymysql
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

USER = "root"
PASSWORD = config.password
HOST = "127.0.0.1"
PORT = "3306"
DATABASE = "alegorithm_db"

CONN = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

sql_engine = sql.create_engine(CONN)

################################################################
#                        Flask Routes                          #
################################################################

@app.route("/")
def home():
    return render_template("verification.html")


@app.route("/index.html")
def index():
    return render_template("index.html")

# --------------------------------------------------------------#
#                       recommender routes                     #
# --------------------------------------------------------------#

@app.route("/recommender.html")
def recommender():
    TABLENAME = "ba_beerstyles"
    query = f"SELECT DISTINCT Category FROM {TABLENAME}"
    df = pd.read_sql_query(query, sql_engine)
    categories = df["Category"].tolist()
    categories.insert(0, "Choose a Category")
    return render_template("recommender.html", categories=categories)


# populate beerstyle dropdown - * Needs work(Dynamic Dropdown) *
@app.route("/beerstyle_names")
def beer_style():
    TABLENAME = "ba_beerstyles"
    query = f"SELECT DISTINCT Style FROM {TABLENAME}"
    df = pd.read_sql_query(query, sql_engine)
    # return json of the dataframe
    return Response(df.to_json(orient="records"), mimetype="application/json")

# populate beerstyle dropdown based upon Category input
@app.route("/beerstyle_filtered/<category>")
def beer_style_filtered(category):
    TABLENAME = "ba_beerstyles"
    query = f"SELECT Style FROM {TABLENAME} WHERE Category = '{category}'"
    df = pd.read_sql_query(query, sql_engine)
    df2 = pd.DataFrame({"Style": ["Select a Beer Style"]})
    df = df2.append(df)
    # return json of the dataframe
    return Response(df.to_json(orient="records"), mimetype="application/json")

# selector for beerstyle for gaugechart
@app.route("/beerstyle/<beerstyle>")
def guagechart(beerstyle):
    TABLENAME = "ba_beerstyles"
    query = f"SELECT * FROM {TABLENAME} WHERE Style = '{beerstyle}'"
    df = pd.read_sql_query(query, sql_engine)
    # return json of the dataframe
    return Response(df.to_json(orient="records"), mimetype="application/json")


# route to display top 5 beer recommendations
@app.route("/recommender/<beerstyle>")
def selector(beerstyle):
    TABLENAME1 = "top_5_beers"
    TABLENAME2 = "final_beers"
    query = f"select {TABLENAME2}.*, {TABLENAME1}.avg_rating, {TABLENAME1}.review_count from {TABLENAME2} cross join {TABLENAME1} on {TABLENAME1}.beer_id = {TABLENAME2}.beer_id where {TABLENAME1}.beer_style = '{beerstyle}'"
    df = pd.read_sql_query(query, sql_engine)
    isempty = df.empty
    if isempty == True:
        df2 = pd.DataFrame(
            {"beer_name": ["Sorry, we dont have a recommendation for that style"]}
        )
        df = df2.append(df)
    # return json of the dataframe
    return Response(df.to_json(orient="records"), mimetype="application/json")


# route to generate wordcloud for top beerstyles
@app.route("/category")
def top_beerstyles():
    TABLENAME = "final_beers"
    query = f"SELECT COUNT(beer_style) AS count, beer_style, category FROM {TABLENAME} GROUP BY beer_style, category"
    df = pd.read_sql_query(query, sql_engine)
    # return json of the dataframe
    return Response(df.to_json(orient="records"), mimetype="application/json")


# route to add beerstyle image
@app.route("/beerstyles_links/<beerstyle>")
def beer_style_links(beerstyle):
    TABLENAME = "beer_styles_links"
    query = f"SELECT * FROM {TABLENAME} WHERE beer_style = '{beerstyle}'"
    df = pd.read_sql_query(query, sql_engine)
    # return json of the dataframe
    return Response(df.to_json(orient="records"), mimetype="application/json")

# --------------------------------------------------------------#
#                       dashboard routes                       #
# --------------------------------------------------------------#

@app.route("/dashboard.html")
def dashboard():
    return render_template("dashboard.html")


@app.route("/state_data")
def state_data():
    TABLENAME = "us_state_data"
    query = f"SELECT * FROM {TABLENAME}"
    df = pd.read_sql_query(query, sql_engine)
    # return json of the dataframe
    return Response(df.to_json(orient="records"), mimetype="application/json")


@app.route("/style_rank")
def style_rank():
    TABLENAME = "beer_style_pop"
    query = f"SELECT beer_style, review_count FROM {TABLENAME} ORDER BY review_count DESC LIMIT 10"
    df = pd.read_sql_query(query, sql_engine)
    # return json of the dataframe
    return Response(df.to_json(orient="records"), mimetype="application/json")


@app.route("/category_data")
def category_data():
    TABLENAME = "ba_beerstyles"
    query = f"SELECT * FROM {TABLENAME}"
    df = pd.read_sql_query(query, sql_engine)
    # return json of the dataframe
    return Response(df.to_json(orient="records"), mimetype="application/json")

# state selector
@app.route("/statedata/<state>")
def state_stat(state):
    TABLENAME = "us_state_data"
    query = f"SELECT * FROM {TABLENAME} WHERE state = '{state}'"
    df = pd.read_sql_query(query, sql_engine)
    # return json of the dataframe
    return Response(df.to_json(orient="records"), mimetype="application/json")


# --------------------------------------------------------------#
#                       breweries routes                       #
# --------------------------------------------------------------#
@app.route("/breweries.html")
def breweries():
    return render_template("breweries.html")


# --------------------------------------------------------------#
#                       recommender model routes                #
# --------------------------------------------------------------#

@app.route("/search.html")
def recommender_selector():
    beers = beers_df['name'].tolist()
    beers.sort()
    beers.insert(0, "Choose a Beer")
    return render_template("search.html", beers = beers)


@app.route("/neighbors/<beer_name>")
def nearest_neighbors(beer_name):
    beer_raw_id = get_beer_raw_id(beer_name)
    df = get_beer_recc_df (beer_raw_id)

    # return json of the dataframe
    return Response(df.to_json(orient = "records"), mimetype='application/json')

@app.route("/predict", methods=["POST"])
def predict():
    data_dict = request.get_json()

    username = data_dict["username"]
    beer_name = data_dict["beer"]
    beer_raw_id = get_beer_raw_id(beer_name)
    predict = algo.predict(username, beer_raw_id)
    df_predict = pd.DataFrame([predict], columns=['username', 'beer_id', 'r_ui', 'estimate', 'details'])
    return Response(df_predict.to_json(orient = "records"), mimetype='application/json')
    

################################################################
#                           Main                               #
################################################################
if __name__ == "__main__":
    app.run(debug=True)