import re
import string
import tqdm

def preprocessing_pipeline(documents_path, labels_path, vocabulary_path, max_features= None, df_min_freq=0,
                           df_max_freq=1.0, remove_punctuation=True, punctuation=string.punctuation,
                           lemmatize=True, remove_stopwords=True, stopword_list='english', min_words_docs=0):

    docs = [line.strip() for line in open(documents_path, 'r').readlines()]
    if remove_punctuation:
        docs = [doc.translate(str.maketrans(punctuation, ' ' * len(punctuation))).replace(' '*4, ' ').
                    replace(' '*3, ' ').replace(' '*2, ' ').strip() for doc in docs]
    if remove_stopwords:
        if type(stopword_list) == list:
            stopwords = set(stopword_list)
        else:
            stopwords = set(stopword_list) #da fixare
        docs = [' '.join([w for w in doc if w in stopwords]) for doc in docs]



