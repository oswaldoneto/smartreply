import json

from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer


def predict(text):

    # let o dataset
    with open('/Users/oswaldo/complain.json') as data:
        data = json.load(data)

    # Get the number of reviews based on the dataframe column size
    num_complain = len(data)

    # Initialize an empty list to hold the clean complain
    clean_train_complain = []
    target_problem_type = []
    for complain in data:
        clean_train_complain.append(complain['title'])
        target_problem_type.append(complain['category'])

    vectorizer = CountVectorizer(analyzer="word",
                                 tokenizer=None,
                                 preprocessor=None,
                                 stop_words=None,
                                 max_features=500)

    train_data_feature = vectorizer.fit_transform(clean_train_complain).toarray()

    # Initialize a Random Forest classifier with 100 trees
    forest = RandomForestClassifier(n_estimators=100)

    # Fit the forest to the training set, using the bag of words as
    # features and the sentiment labels as the response variable
    #
    # This may take a few minutes to run
    forest = forest.fit(train_data_feature, target_problem_type)

    clean_test_complain = []

    clean_test_complain.append(text)

    test_data_features = vectorizer.transform(clean_test_complain)
    test_data_features = test_data_features.toarray()

    result = forest.predict(test_data_features)

    return result


