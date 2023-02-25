# Twitter_Pipeline
Development of automated data pipelines to extract twitter data, with a sentiment analysis 

## Table of contents
- [Tech stack](https://github.com/Dorad-H/Twitter_Pipeline/blob/master/README.md#tech-stack)
- [ETL pipleline](https://github.com/Dorad-H/Twitter_Pipeline/blob/master/README.md#extract-transform--load)
- [ELT pipeline](https://github.com/Dorad-H/Twitter_Pipeline/blob/master/README.md#extract-load--transform)
- [Machine Learning](https://github.com/Dorad-H/Twitter_Pipeline/blob/master/README.md#machine-learning)
- [Authors](https://github.com/Dorad-H/Twitter_Pipeline/blob/master/README.md#authors)

## Tech stack
The following were used due to being free, open source and therefore accessible for the team to use.
- Python

  - Allows access to the twitter API for extraction of data
- Apache Airflow

  - Automates and monitors workflows.
- PostgreSQL

  - Secure and scalable database in which data can be queried for use.

## Extract, Transform & Load
Used for structured data, transformed within python to conform to the below model to ensure the database remained efficient and sacable in future.
![alt text](https://github.com/Dorad-H/Twitter_Pipeline/blob/f2fb2f6d67c421ec0cf907aef06637455465ecac/ER%20diagram.png "ER Diagram")

## Extract, Load & Transform
Used for semi-structured data, relevant variables extracted in JSON format. Stored in the database in the below format which could then be extracted and transformed for needed use.
![alt text](https://github.com/Dorad-H/Twitter_Pipeline/blob/917c0e72d1e1e96f7d7d9f3a6674ee1d35b355e6/Semi%20structured.png "JSON format")

## Machine Learning
Sentiment analysis of company tweets using the [VADER package.](https://github.com/cjhutto/vaderSentiment) Sentiment of tweets scored using this package -1 to 1 with the following groupings shown below:
- Negative
- Neutral (-0.05 to 0.05)
- Positive

Logistic Regression used to predict the sentiments by a company
- Accuracy of 72%
- F1 score of 0.75 on positive values

# Authors
- [Dorad Hasani](https://studentsunionucl.org/sites/default/files/u198411/image00060.jpeg)
- [Jan Salcedo](https://github.com/SuperSalcedo22)
- [Pernelle Gamrowski](https://github.com/pernelleg)
- [Helen Luhaäär](https://github.com/HelenLB)


[Back to the top](https://github.com/Dorad-H/Twitter_Pipeline/blob/master/README.md#twitter_pipeline)
