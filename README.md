# Twitter Pipeline and Sentiment Analysis

Development of automated data pipelines to extract twitter data, with a sentiment analysis

## Table of contents

-   [Description](https://github.com/Dorad-H/ELT-Twitter-Sentiment-Analysis#tech-stack)
-   [ELT pipeline](https://github.com/Dorad-H/ELT-Twitter-Sentiment-Analysis#extract-load--transform)
-   [Machine Learning](https://github.com/Dorad-H/ELT-Twitter-Sentiment-Analysis#machine-learning)
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

Used for semi-structured data, relevant variables extracted in JSON format. Stored in the database in the below format which could then be extracted and transformed for needed use.
![alt text](https://github.com/Dorad-H/Twitter_Pipeline/blob/917c0e72d1e1e96f7d7d9f3a6674ee1d35b355e6/Semi%20structured.png "JSON format")

###### <div align="center"> Figure 1: Entity-relationship model </div>

## Machine Learning

Sentiment analysis of company tweets using the [VADER package.](https://github.com/cjhutto/vaderSentiment) Sentiment of tweets scored using this package -1 to 1 with the following groupings shown below:

-   Negative
-   Neutral (-0.05 to 0.05)
-   Positive

Logistic Regression used to predict the sentiments by a company

-   Accuracy of 72%
-   F1 score of 0.75 on positive values

# Authors

-   [Dorad Hasani](https://github.com/Dorad-H)
-   [Jan Salcedo](https://github.com/SuperSalcedo22)
-   [Pernelle Gamrowski](https://github.com/pernelleg)
-   [Helen Luhaäär](https://github.com/HelenLB)

[Back to the top](https://github.com/Dorad-H/ELT-Twitter-Sentiment-Analysis#twitter_pipeline)
