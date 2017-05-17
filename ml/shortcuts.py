import os
import json
import re

from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from unicodedata import normalize

from smartreply.settings import BASE_DIR


def predict(text):

    # let o dataset
    dataset_file = os.path.join(BASE_DIR, 'dataset', 'complain.json')

    with open(dataset_file) as data:
        data = json.load(data)

    # Get the number of reviews based on the dataframe column size
    num_complain = len(data)

    # Initialize an empty list to hold the clean complain
    clean_train_complain = []
    target_problem_type = []
    for complain in data:
        clean_train_complain.append(clean_data(complain['complain']))
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

    clean_test_complain.append(clean_data(text))

    test_data_features = vectorizer.transform(clean_test_complain)
    test_data_features = test_data_features.toarray()

    result = forest.predict(test_data_features)

    return result


def clean_data(pure_text):


    def clean_properties(pure_text):
        """
        Remove things like 'RA: NA123-10' 'E-mail: bla@email.com'          
        """
        clean_data = re.sub('([\wZáéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ-]+)(?:\:\s).+', ' ', pure_text)
        return clean_data

    def clean_email(pure_text):
        """
        Remove things like 'bla@email.com'          
        """
        clean_data = re.sub(r'[\w\.-]+@[\w\.-]+', ' ', pure_text)
        return clean_data

    def clean_pontuation(pure_text):
        """
        Remove things like '. : , -'          
        """
        clean_data = re.sub(u'[^a-zA-ZáéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]', ' ', pure_text)
        return clean_data

    def clean_words_with_number(pure_text):
        """
        Remove things like 'N278A9'          
        """
        clean_data = re.sub(r'\w*\d\w*',' ', pure_text )
        return clean_data

    def clean_lower(pure_text):
        return pure_text.lower()

    def clean_single_white_space(pure_text):
        return ' '.join(pure_text.split())

    def clean_stop_words(pure_text):
        stops = stopwords.words('portuguese')
        meaningful_words = [word for word in pure_text.split() if not word in stops]
        return ' '.join(meaningful_words)

    def clean_greeting_words(pure_text):
        greeting_words = ['ola', 'olá', 'oi', 'bom-dia', 'boa-tarde', 'boa-noite', 'boa', 'noite', 'tarde', 'dia']
        meaningful_words = [word for word in pure_text.split() if not word in greeting_words]
        return ' '.join(meaningful_words)

    def clean_acentos(pure_text):
        return normalize('NFKD', pure_text).encode('ASCII', 'ignore').decode('ASCII')


    clean_data = clean_properties(pure_text)

    clean_data = clean_words_with_number(clean_data)

    clean_data = clean_email(clean_data)

    clean_data = clean_pontuation(clean_data)

    clean_data = clean_lower(clean_data)

    clean_data = clean_single_white_space(clean_data)

    clean_data = clean_stop_words(clean_data)

    clean_data = clean_greeting_words(clean_data)

    clean_data = clean_acentos(clean_data)

    return clean_data






