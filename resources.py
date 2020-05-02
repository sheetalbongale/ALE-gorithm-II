import os
import pandas as pd
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


def get_beers_list ():
    beer_list = beers_df['name'].tolist()
    return beer_list

def get_neighbors (beer_name):

    beer_raw_id = beers_df.loc[beers_df.name==beer_name,'beer_id'].values[0]
    
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