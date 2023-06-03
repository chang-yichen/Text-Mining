import pandas as pd
import csv

df = pd.read_csv("small_df.csv",delimiter=',')

feature_df = pd.read_csv("tfidf_matrix.csv",delimiter=',')
feature_df.drop(columns=['Unnamed: 0'], inplace=True)

# load the URL data
url_dict = pd.read_csv("restaurant_url.csv", header=None, index_col=0)
url_dict = url_dict[1].to_dict()
# delete the header
del url_dict['Restaurant']

with open("Summaries_of_restaurants.csv", "r", newline="") as csvfile:
  reader = csv.reader(csvfile)
  summary = {}
  summ = []
  for row in reader:
    summ.append(row[1])
  i=1
  for key in df:
    summary[key] = summ[i]
    i = i+1

def initilizing():
    corpus = []#all possible valid input words 
    for key in feature_df:
        corpus.append(key)

    return corpus

#rank all restaurants, get their scores, which store in 'ranks'
#input:a list of string(words from all filters)
#output:a dictionary, value is the score of restaurant
def ranking(filter_words, corpus):
    ranks = {}
    for key in df:
        ranks[key] = 0
    for word in filter_words: 
        if(word in corpus): 
            n=0
            i=0
            for key in ranks:
                ranks[key] = (n*ranks[key]+feature_df[word][i])/(n+1)
                i=i+1
            n = n+1
    return ranks


#used by submit and next button
#input:next_time is default when first time called , and a list of four filter words
#next_time is the time that next button is pressed
#output:a string(name of a restaurant)
def submitting_and_next(filter_words=[], next_time=0):
    corpus = initilizing()
    ranks = ranking(filter_words, corpus)
    #pick the (next_times+1)th best restaurant
    for i in range(next_time+1):
        recommend = "十六區和風料理"
        highest_score = ranks["十六區和風料理"]
        for key in ranks:
            if (ranks[key] > highest_score):
                recommend = key
                highest_score = ranks[key]
        ranks[recommend] = 0

    if(highest_score == 0):
        return {"Restaurant":"No other recommendation","Summary":"NULL"}
    return {"Restaurant":recommend,"Summary":summary[recommend], "URL":url_dict[recommend]}