# Predicting Social Unrest Events Caused By Elections

- Arvind Ramachandran (@RvI101)
- Dhayanidhi Gunasekaran (@dnidhi2710)
- Navaneethakrishnan Ramanathan (@sudonav)


## Problem Statement
The goal is to observe events with the present and historical data and predict events of social unrest attributed to election violence.
 Social Media, and News are two sources of vast data that are publicly available that can be used for detecting and forecasting events

*Focus Area: India*


## Data Collection	
Data was scraped from the published **The Hindu**
59,385 articles published between 1st Jan 2019 and 31st Mar 2019 available in **The Hindu’s** online archive were collected.
Relevant Tweets for every article(after preprocessing) was also collected and sentiment analysis was performed
ACLED dataset was used for benchmarking and evaluation

## Data preprocessing
### ACLED
The ACLED data was parsed and word frequency was computed
Bag of words was formed with the most frequently occurring words after,
- Removing Stop words
- Stemming
- Lemmatization
- Removing punctuations

These keywords were used for filtering the relevant articles.

Articles with >2 keywords were categorized as politically relevant.

### NEWS Articles
The articles were subjected to,
- Removing Stop words
- Stemming
- Lemmatization
- Removing punctuations

Rule-based matching is performed on article body using spaCy and custom rules in order to label articles as 1 or 0 to aid training a classifier.
The Custom Rules are aimed at matching sentences which show intent to organize a planned protest or social unrest gathering.


## Custom Rules for Rule-Based Matching
`spaCy`’s token matching was decided on as it allows for inexact matches which is absolutely necessary to be functional.

A list of phrases was manually assembled. Each phrase consists of a verb lemma and a noun lemma.

Verb list : ['organize', 'plan', 'announce', 'prepare', 'demand', 'stage', 'call', 'hold']

Noun list : ['demonstration', 'march', 'protest', 'strike', 'bandh', 'dharna', 'union', 'riot', 'march', 'gathering', 'attack']

Phrase list was then constructed by cartesian product of these two lists.

The rules are basically simplified proximity matching of two words within a sentence.

``` 
Pattern_1 = [{'LEMMA': verb_i, 'POS': 'VERB'},
           {'IS_ALPHA': True, 'OP': '*'},
           {'LEMMA':noun_i, 'POS': 'NOUN'}]
Pattern_2 = [{'LEMMA': noun_i, 'POS': NOUN},
           {'IS_ALPHA': True, 'OP': '*'},
           {'LEMMA':verb_i, 'POS': VERB}]
```

**Example Match**

The banned ***CPI (Maoist) has called for a bandh*** on _April 5_ in the Visakha Agency in protest against the alleged killing of two tribal farmers by the anti-Naxal force, the Greyhounds. According to the Maoists, the two were innocent farmers and not its members as claimed by the security forces. Batti Bhushanam (52) and Sidaari Jamadhar (30) were reportedly killed on March 15 near Buradamamidi village in the Pedakodapalle panchayat of the Pedabayulu mandal in the district. In a letter released on Saturday, the Maoists also claimed that the TDP government was using repressive tactics through the security forces to exploit the natural resources in the tribal areas. The letter, addressed by MKVB (Malkangiri-Koraput-Visakhapatnam Border) Division secretary Kailasam, said the security forces were arresting and torturing innocent tribals.

The previously shown rules will match **‘called for a bandh’** in this article text. April 5 is also recognized as a **DATE** entity in this same sentence by the Entity Recognizer packaged with the spaCy english model. Dates are assumed to be close to the matched phrase and the first such nearby entity is extracted.

## Data preprocessing - Extract Features
A list of Organizations/Groups/People are extracted from each article to form a list of Actors using Named Entity Recognition.
The extracted DATE entities are derived into absolute dates using the published date of the article. For example: ‘5 days’ => DatePublished + 5 days.
Using a Tweet scraper, relevant Tweets published within a 50 day window of the article being published are mined for sentiment scores. Three numbers are derived - % of positive tweets, % of neutral tweets and % of negative tweets. These are added to the article featureset.


## Dataset Split
Articles from Jan 2019 to Mar 2019 are used as the training dataset and validation set. (59340 count)
Articles from Apr 2019 are used as test dataset. (13526 count)

# Modelling - Features
The article text is vectorized using only the important keywords.
The location feature is also considered as certain locations may be more prone to social unrest events than others(usually due to population or socio-economic factors). It is broadened into a bounding box and appropriately prior weighted to reduce its impact.
Sentiment scores were also added as feature to the data

## Models Used
- Naive Bayes - The go-to method for simple text classification
- Logistic Regression - Excellent for binary classification
- SGD
- Support Vector Machine - Helpful for text classification as it reduces the need for labeled training instances

## Statistics

|Metrics|SGD Classifier|GaussianNB|Logistic Regression|SVM|
|-------|--------------|----------|-------------------|---|
|Accuracy|.85|.83|.90|.92|
|Precision|.94|.94|.89|.94|
|Recall|.75|.75|.83|.91|
|F1 Score|.83|.83|.86|.93|

The average lead time is 4.4 days in the test data

# Improvements
Tune the model to predict based on specific domains and drill deep into causal events inside Politics
Create a data pipeline to obtain, clean data from all possible sources and create an integrated data source
Employ more rigorous methods to extract date entity



**Take Away Points**
- Great Hands on experience in Text and web Mining
- Learned many data cleaning and Preprocessing Techniques
