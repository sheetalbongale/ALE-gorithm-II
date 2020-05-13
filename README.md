# ALE-gorithm-II - Drink Good Beer
### Recommender Web-app & Educational Dashboard for all things beer!🍺

![beers gif](static/img/BeerExplosion.gif)


### Group Members: 
```
+ Barry Haygood - Project manager
+ Sheetal Bongale - Lead Developer
+ Cathy Egboh
+ Catherine Gomes
+ Maya Saeidi
+ Michelle Brucato
+ Sahar Mohammadi
```

<details>
    <summary><b>Project Requirements - Click the drop down!</b>  🔽</summary>

+ Proposal
    + Must submit a one-page proposal before starting

+ Core App
    + Must use HTML
    + Must use Flask or FastAPI
    + Must use a scikit-learn model
    + May use a database - not required
    + May use R to select models, but final models must be in Python

+ Routes
    + Must have a home route that uses a Jinja template
    + Must have a route that takes in user data and returns a prediction
    + May have routes that collect data from the user and send it to a database
    + May have a route that uses Plotly or D3 for visualization in a Jinja template
    + May have a route that accesses, filters, and serves data from the database as a JSON
    + May have a route that dynamically filters and displays data to the UI

+ Testing
    + Use Postman with at least one request per route

+ Deployment
    + Must be deployed (Heroku, GCP, etc...)
    + Must use Pipenv

+ Repo
    + The repo must have a properly formatted README.md
    + Code must be formatted with Black and prettier.js where appropriate
    + Must have at least 5 Github Issues

+ Presentation
    + Prepare a seven-minute presentation (Possibly adjusted epending on number of groups and size of each group)

+ Individual
    + Every member must make at least 5 commits that are eventually merged to master
    + Every member must write code that solves at least one meaningful Github Issue

</details>

## What is ALE-gorithm?
Have you ever wandered down the beer aisle feeling overwhelmed by options? Do you have a thirst for deliciously brewed craft beer, but don’t know which to choose?
Then you’ve come to the right place!
The goal of the ALE-gorithm recommender web application is to recommend and match a user to the best brews out there and to educate consumers on the craft beer space including styles, flavor profiles.

### Features
🟡<b> Beer Recommender:</b>
Are you a beer connoisseur? Or even new to the #beerlife experience? No matter what your level of expertise is, if you love to partake in a nice "cold one", then check out the recommender page. 
We have scanned over a million beers and will match you to the top beers that best suit your palette.  ALE-gorithm will recommend your next beer in two ways using a custom recommender model built with Surprise!.  See below for more details! 

🟡<b> Beer Analysis and Educator:</b>
Want to learn more about your favorite beers? 
Our interactive analysis page offers information about beers and breweries to both novice and seasoned beer lovers a like. 

🟡<b> Find breweries near you:</b>
Looking for a fun beer night or taste some new craft beers? Search to find all the breweries around you or any city around the world!

### More about the Machine Learning Algorithms used in this project:
**ALE-gorithm** utilizes machine learning to create recommendations for beers based upon user reviews.  In the first project ([Find it here](https://github.com/sheetalbongale/ALE-gorithm)),  a simple sorting algorithm was utilized to suggest the top five beers for a user based upon the category and style of beer and the beer’s average overall score.  **ALE-gorithm 2** personalizes the recommendation based upon the unique inputs of each user by using the KNNBasic model with [Surprise](http://surpriselib.com/), a Python scikit focused on creating recommender systems.

In order to create the model,  the original dataset of over 8 million reviews had to be substantially reduced.  Pandas was utilized to randomly sample 4 million reviews and then only beers that had at least 500 reviews were selected.  This reduced the dataset to 1.2M reviews with 1182 beers from 271 different breweries.

Surprise was then used to evaluate and develop a model that could accurately predict the rating for each user.  Several prediction algorithms were evaluated including *KNNBasic, SVD, SlopeOne,* and *CoClustering*.  NLP Content based recommender system were also developed and tested using TfidfVectorizer, CountVectorizer and NLTK Library to find the cosine_similarity matrix for the user descriptive reviews.
*KNNBasic* was selected for its overall prediction accuracy as measured by root mean square error (RMSE) in addition to mean absolute error (MAE) and its ability to predict similarity of items (beers).  The similarity prediction was optimized by comparing the output of the cosine, pearson, and pearson_baseline similarity measures and selecting the measure that returned beers that were most alike in terms of style, brewery, and rating.  Pearson_baseline was found to produce the best results.

There are two models used to recommend your next beer.  

- The first utilizes the similarity model in Surprise to return the five nearest neighbors for a given beer.  In practical terms, this prediction is similar to the commonly found recommenders online that will suggest a similar item to a consumer’s selection.

- The second model predicts the rating for all 1182 beers in the dataset for a given user and then returns the top 10 highest predicted ratings and the bottom 10 predicted ratings utilizing collaborative filtering k-Nearest Neighbor (KNN).  This is a customized recommendation for any user in the database and a great way for a user to find their next perfect beer!

### Deployment:
ALE-gorithm is deployed on GCP > **[ALE-gorithm 2](https://alegorithm2-fxljyqhslq-uc.a.run.app/)**

### Technologies used to build ALE-gorithm:
```
- App Back-End: Python Flask | SQLAlchemy | scikit-Surprise
- Database: MySQL | Google Cloud Platform (GCP) 
- Data Visualization: Javascript | Plotly.js | D3.js | AnyChart.js
- Front-End: HTML | Bootstrap | CSS
- Web-Scraping: Requests, Beautiful Soup
- Testing: Postman
```

### Data Sources:
- [Beer Advocate Kaggle Dataset](https://www.kaggle.com/ehallmar/beers-breweries-and-beer-reviews/activity)

### Additional Data Resources:
* [BeerAdvocate](https://www.beeradvocate.com)
* [CraftBeer](https://www.craftbeer.com)
* [Brewers Association ](https://www.brewersassociation.org)
* [RateBeer](https://www.ratebeer.com)

# Cheers! 🍻

### Copyright 
Team Ale-gorithm © 2020 | UT Data Analysis and Visualization Nov 2019 - May 2020
