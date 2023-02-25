'''Importing the required packages'''

import tweepy
from tweepy import *
import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import datetime
import ast
from airflow import DAG
from airflow.operators.python_operator import PythonOperator 
from datetime import datetime,timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#Defining the arguments for the DAG

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'email_on_failure':False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

#Defining the DAG which will be used for all tasks

dag = DAG(
    'twitter_flow_dag',
    default_args = default_args,
    description = 'Collecting tweets dag',
    schedule_interval = timedelta(minutes=1)
)

'''
defining the credentials for pgAdmin from the env file
'''
# Host
pg_host=os.getenv('HOST')
# Port
pg_port=os.getenv('PORT')
# Database
pg_db=os.getenv('DATABASE')
# User
pg_user=os.getenv('USER')
# Password
pg_pass=os.getenv('PASSWORD')
# Get the table name from the env file
table_name = os.getenv('TABLE_NAME')

def sentiment_evaluation(sentence):
    '''Initialises the vader sentiment function then outputs the compound polarity score'''

    # Create a SentimentIntensityAnalyzer object
    sid_object = SentimentIntensityAnalyzer()

    # Uses the sentiment diction to output a polarity score
    sentiment_diction = sid_object.polarity_scores(sentence)
    
    return sentiment_diction['compound']

# Commenting this part out of the code for now 
#     # decide sentiment as positive, negative and neutral. Can be tweaked as seen fit
#     if sentiment_diction['compound'] >= 0.05:
#         return "Positive"
 
#     elif sentiment_diction['compound'] <= - 0.05 :
#         return "Negative"
 
#     else:
#          return "Neutral"

tweet_id = [] # stores the id in a separate container
data = [] # creates an empty list to store the data in
replies = [] #empty list to find the replies

def extract_twitter(**kwargs):
    '''The function needed to extract data from the twitter API'''
    load_dotenv()
    # accessing  API key and secret
    consumer_key = os.getenv('API_KEY')
    consumer_secret = os.getenv('API_SECRET')
    access_token = os.getenv('TOKEN')
    access_token_secret = os.getenv('TOKEN_SECRET')
    
    # Authenticating the keys
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    # Creating the API object
    api = tweepy.API(auth)
    
    accounts = ['@amazon','@ferrari','@GoogNmicro','@NFL','@NintendoUK','@pepsi','@tacobell','@SpaceX']
    
    # iterate through all accounts in the list
    for account in accounts:
        # loop that goes through each recent tweet by the user
        for tweet in tweepy.Cursor(api.user_timeline, screen_name=account, 
                                    tweet_mode="extended",exclude_replies=True).items(10):


            # storing the tweet id into a different list
            tweet_id.append(tweet.id)

            # for each tweet found, extracting the replies
            rep = api.get_status(tweet.id,tweet_mode="extended",wait_on_rate_limit=True)

            # finds the replies to the tweet
            for tweet2 in tweepy.Cursor(api.search_tweets, q='to:{}'.format(account), 
                               since_id=tweet.id, tweet_mode='extended').items():
                # if it is a reply, writes to a dictionary within the list
                # with each item containing the text and number of likes
                if tweet2.in_reply_to_status_id == tweet.id:
                    replies.append({'Rep_text':tweet2.full_text,
                                    'Rep_likes': tweet2.favorite_count
                                   })

            # creates a dictionary within the list of all the data needed and changes to string to store in pgadmin4
            data.append(str({
                # User id of the tweeter
                "User_ID":tweet.user.id,
                # when the tweet was created
                'Time': tweet.created_at.timestamp(),
                # the text of the tweet itself
                'Text': tweet.full_text,
                # number of likes/favourites the tweet got
                'Favorites': tweet.favorite_count,
                # number of retweets
                'Retweets': tweet.retweet_count,
                # Any hashtags within the tweet
                'Hashtags': [hashtag["text"] for hashtag in tweet.entities.get("hashtags")],
                # the screen name of users mentioned in the tweet
                'Mentions': [user["screen_name"] for user in tweet.entities.get("user_mentions")],
                # urls linked inside the tweet
                'URLs': [url["expanded_url"] for url in tweet.entities.get("urls")],
                # replies to the tweet
                'Replies':replies
            }))

        # store the data into a dataframe
        df = pd.DataFrame({'tweet_id':tweet_id,
                           'tweet_info':data})
        result_json = df.to_json(orient='split')
        ti = kwargs['ti']
        ti.xcom_push(key='dataframe', value=result_json)
        return result_json
    
# Task 1 - extracting

task_extracting = PythonOperator(
    task_id='twitter_airflow',
    python_callable=extract_twitter,
    provide_context = True,
    do_xcom_push = True,
    dag = dag
)
        
def store_postgres(**kwargs):
    '''Taking the data from python and storing within a postgresql database'''

    # Connecting to the database for querying
    conn = psycopg2.connect(
        host=pg_host,
        database=pg_db,
        user=pg_user,
        password=pg_pass,
        port=pg_port
    )
    
    # creating the cursor to execute the queries
    cur = conn.cursor()
    
    # Execute a SELECT statement to extract id from the table
    cur.execute(f"SELECT tweet_id FROM {table_name}")
    
    # change the rows into a list to be iterated through
    db_id = cur.fetchall()
    
    # change the rows into a list to be iterated through
    db_id = cur.fetchall()

    #Definging the xcom pull
    ti=kwargs['ti']
    json_pull=ti.xcom_pull(key='dataframe',task_ids='twitter_airflow')

    df = pd.read_json(json_pull, orient='split')
    
    # checks if the value is inside the list
    check = df['tweet_id'].isin(db_id)
    
    # uses boolean indexing to remove the rows that fit the condition
    filtered = df[~check]

    # Close the cursor and connection
    cur.close()
    conn.close()

    # Creating the engine to connect to postgres in order to alter tables
    engine = create_engine(
        f'postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    
    # Insert information into the table
    filtered.to_sql(table_name, engine, if_exists='append', index=False)
    
#Task 2 - loading data

task_loading = PythonOperator(
    task_id='twitter_db',
    python_callable=store_postgres,
    provide_context=True,
    dag = dag
)
   
def transform():
    '''Function that extracts the data from the sql database and transform for use'''
    
    # Creating the engine to connect to postgres
    engine = create_engine(
        f'postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    
    # Read the entire table into a pandas dataframe
    global df
    df = pd.read_sql_table(f'{table_name}', engine)
    
    # Use the 'apply' method to convert the column back into a dictionary
    df['json_info'] = df['tweet_info'].apply(lambda x: ast.literal_eval(x))
    
    # creating empty lists to extract the data from the dictionary to be put into lists
    user_id = []
    time = []
    text = []
    likes = []
    retweets = []
    hashtags = []
    mentions = []
    urls = []
    no_replies = []
    replies = []
    
    # for loop to extract data from the dictionary and add to lists
    for val in df['json_info']:
        user_id.append(val['User_ID'])
        time.append(val['Time'])
        text.append(val['Text'])
        likes.append(val['Favorites'])
        retweets.append(val['Retweets'])
        hashtags.append(len(val['Hashtags']))
        mentions.append(len(val['Mentions']))
        urls.append(len(val['URLs']))
        no_replies.append(len(val['Replies']))
        replies.append(val['Replies'])
    
    # writes the list into the dataframe for use
    df['User_id'] = user_id
    df['Time'] = time
    df['Text'] = text
    df['Likes'] = likes
    df['No_retweets'] = retweets
    df['No_Hashtags'] = hashtags
    df['No_Mentions'] = mentions
    df['No_URLs'] = urls
    df['No_replies'] = no_replies
    df['Replies'] = replies
    
    # removing the old json format from the table
    df.drop(columns=['tweet_info','json_info'],inplace=True)
        
    # initialising empty list for the score
    vader_score = []

    # goes through each tweet by the account
    for all_reps in df['Replies']:
        retweet = []
        rep_likes = []
        rep_score = []

        # goes through all the replies for the tweet
        for dicts in all_reps:
            # cleans the tweet
            retweet.append(dicts['Rep_text'])
            rep_likes.append(dicts['Rep_likes'])

        # vader analysis of each tweet
        rep_score = [sentiment_evaluation(text) for text in retweet]

        # multiplying the vader score by the like count
        for index in range(len(rep_score)):
            rep_score[index] += rep_score[index]*rep_likes[index]

        # finding the average of the lvader scores
        vader_score.append(sum(rep_score)/sum(rep_likes))
        
    # Updating the dataframe with the found vader score for each tweet in the database
    df['Score'] = vader_score
    
#Task 3 - transforming the data

task_transforming = PythonOperator(
    task_id='twitter_data_transform',
    python_callable=transform,
    provide_context=True,
    dag = dag
)

#Calling the tasks in this sequence Task 1 --> Task 2 --> Task 3, so that they don't all start at once

task_extracting.set_downstream(task_loading)
task_transforming.set_upstream(task_loading)
