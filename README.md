# Twitter Pipeline and Sentiment Analysis

Development of automated data pipelines to extract and store twitter data, used for sentiment analysis

## Table of contents

-   [Description](https://github.com/Dorad-H/ELT-Twitter-Sentiment-Analysis#tech-stack)
-   [ELT pipeline](https://github.com/Dorad-H/ELT-Twitter-Sentiment-Analysis#extract-load--transform)
-   [Sentiment Analysis](https://github.com/Dorad-H/ELT-Twitter-Sentiment-Analysis#machine-learning)
-   [Authors](https://github.com/Dorad-H/ELT-Twitter-Sentiment-Analysis#authors)

## Description

In the age of social media, analyzing user-generated content such as tweets and replies has become a critical component of various businesses and organizations. Sentiment analysis, which involves extracting insights from such data, has become an essential tool in making data-driven decisions. However, before any meaningful analysis can be conducted, the data must first be collected and processed efficiently. This is where an Extract-Load-Transform (ELT) pipeline comes into play.

In this project, we aim to create an ELT pipeline that focuses on extracting Twitter data, specifically tweets and replies to those tweets, storing them in a relational database, transforming the data, and then using it for sentiment analysis. The pipeline will be designed to handle large amounts of data, and will be optimized for speed and efficiency.

By implementing this pipeline, we will be able to analyze the sentiment of tweets and their replies, and gain insights into the public perception of various topics. This can be particularly useful for businesses, political campaigns, and other organizations that want to understand how their products, services, or messages are being received by the public.

### Tech stack

-   #### Python

    Used to create the extract and transform the twitter data as well as do the sentiment analysis.

-   #### Apache Airflow

    Used to Automate and monitor the pipeline.

-   #### PostgreSQL
    A relational database Used to store the transformed data.

## Extract, Load & Transform

This ELT pipeline involves using Tweepy, the Twitter API, to extract data from Twitter, specifically tweets and replies. The data is retrieved is in a semi-structured format and is stored into a PostgreSQL database. The data is then extracted and transformed using pandas, a popular data manipulation library in Python, where it is cleaned and reformated into a structured format to fit the requirements of the machine learning project discussed later.

The pipeline is designed to be automated and monitored using Apache Airflow, an open-source platform for creating, scheduling, and monitoring workflows. We define the pipeline as a DAG (Directed Acyclic Graph), were we schedule of tasks, defined as python functions, and monitor progress. This makes the pipeline more efficient, reliable, and scalable, which is essential when working with large volumes of data.

## Sentiment Analysis

The purpose of the project is to create a machine learning model that can predict the sentiment of tweets, made by official Twitter accounts of companies like Microsoft and SpaceX, based on its content. The sentiment analysis involves classifying the replies into positive, negative, or neutral categories using the [VADER package](https://github.com/cjhutto/vaderSentiment), and then using the data to train the model. Once trained, the model can be used to predict the sentiment of new tweets, which can be useful for companies to monitor their online reputation and respond to customer feedback in a timely and effective manner. Overall, this project involves applying natural language processing and machine learning techniques to social media data to provide insights into customer sentiment and behavior.

We chose to train and use Logistic Regression to predict the sentiments as it yeilded the highest accuracy score for the given features. Our model achieved the following statistics:

-   Accuracy of 72%
-   F1 score of 0.75 on positive values

## Authors

-   [Dorad Hasani](https://github.com/Dorad-H)
-   [Jan Salcedo](https://github.com/SuperSalcedo22)
-   [Pernelle Gamrowski](https://github.com/pernelleg)
-   [Helen Luhaäär](https://github.com/HelenLB)

[Back to the top](https://github.com/Dorad-H/ELT-Twitter-Sentiment-Analysis#twitter_pipeline)
