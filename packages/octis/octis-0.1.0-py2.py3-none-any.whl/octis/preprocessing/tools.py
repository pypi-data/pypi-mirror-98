import gensim
from sklearn.model_selection import train_test_split
from gensim.utils import simple_preprocess
from octis.dataset.dataset import Dataset
import multiprocessing as mp
import spacy
import string


def create_pool(n_cpu):
    """
    Create a pool

    Parameters
    ----------
    n_cpu : number of processes in the pool

    Returns
    -------
    pool : a pool of n_cpu processes
    """
    pool = mp.Pool(processes=n_cpu)
    return pool


def _multiprocess(pool, n_cpu, function, corpus, arguments=[]):
    """
    Execute a function on a corpus in multicore

    Parameters
    ----------
    pool : pool of n_cpu processes
    n_cpu : number of processesto use
    function : function to execute
    corpus : corpus (usually first argument of function)
    arguments : others arguments of the function

    Returns
    -------
    corpus : the result of the function evaluated on corpus
    """
    corpus_length = len(corpus)
    documents_for_cpu = round(corpus_length/n_cpu) + 1
    tmp_tot = corpus_length
    cumulated_range_interval = 0
    ranges = [0]
    for _ in range(n_cpu):
        if tmp_tot - documents_for_cpu >= 0:
            tmp_tot -= documents_for_cpu
            cumulated_range_interval += documents_for_cpu
            ranges.append(cumulated_range_interval)
        else:
            ranges.append(corpus_length)
    results = [pool.apply(function, args=(
        corpus[ranges[y]:ranges[y+1]], arguments)) for y in range(n_cpu)]
    for y in range(n_cpu):
        corpus[y*documents_for_cpu:y*documents_for_cpu +
               documents_for_cpu] = results[y]
    return corpus


def remove_punctuation(corpus, *_):
    """
    Removes the punctuation in the corpus

    Parameters
    ----------
    corpus : the corpus

    Returns
    -------
    corpus : corpus without punctuation
    """
    corpus = [doc.translate(str.maketrans(
        string.punctuation, ' '*len(string.punctuation))) for doc in corpus]
    return corpus


def create_bags_of_words(corpus):
    """
    Convert each document in the corpus from string
    into a list of words
    Parameters
    ----------
    corpus : corpus in list of strings format

    Returns
    -------
    corpus in list of lists format.
    corpus[document][word]
    """
    for doc in corpus:
        yield(gensim.utils.simple_preprocess(str(doc), deacc=True))


def remove_stopwords(corpus, stop_words):
    """
    Removes the stopwords from the corpus

    Parameters
    ----------
    corpus: the corpus
    stop_words : list of stopwords

    Returns
    -------
    corpus without stopwords
    """
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in corpus]


def lemmatization(corpus, pos):
    """
    Lemmatize the words in the corpus

    Parameters
    ----------
    corpus: the corpus
    pos: pos tags to keep
    Returns
    -------
    result : corpus lemmatized
    """

    nlp = spacy.load("en_core_web_sm")

    result = []
    for document in corpus:
        doc = nlp(" ".join(document))
        if len(pos) > 0:
            result.append([token.lemma_ for token in doc if token.pos_ in pos])
        else:
            result.append([token.lemma_ for token in doc])
    return result


def words_to_remove(corpus, min_word_freq, max_word_freq):
    """
    Find words which
    document/word frequency is less than min_word_freq or
    greater than max_word_freq

    Parameters
    ----------
    corpus : the corpus
    min_word_freq : minimum word/doc frequency in the corpus
    max_word_freq : maximum word/doc frequency in the corpus

    Returns
    -------
    to_remove : list of words with doc/word frequency outside
                the boundaries
    """
    corpus_length = len(corpus)
    #minimum = round(min_word_freq*corpus_length)
    #maximum = round(max_word_freq*corpus_length)
    words_dict = {}
    for document in corpus:
        word_found_in_article = {}
        for word in document:
            if word in words_dict:
                if word not in word_found_in_article:
                    words_dict[word] += 1
                    word_found_in_article[word] = True
            else:
                words_dict[word] = 1
                word_found_in_article[word] = True
    to_remove = {}
    for key, value in words_dict.items():
        word_frequency = float(value)/float(corpus_length)
        if word_frequency <= min_word_freq or word_frequency >= max_word_freq or len(key) < 3:
            to_remove[key] = True
    return to_remove


def filter_words(corpus, words):
    """
    Remove from the documents each occurrence of the words in input

    Parameters
    ----------
    corpus : the corpus
    words : list of words to remove from corpus

    Returns
    -------
    result : corpus without the words to remove
    """
    result = []
    for document in corpus:
        result.append([word for word in document if not word in words])
    return result


def remove_docs(corpus, min_doc=0, labels=[], partition=0,
                edges=[], extra_data="", info={}):
    """
    Remove documents with less than min_doc words
    from the corpus and create a dictioonary with
    extra data about the corpus

    Parameters
    ----------
    corpus : the corpus
    min_doc : optional, default 0
              minimum number of words per document
    labels : optional, list of labels of the documents
    partition : optional, partition of the dataset
    edges : optional, edges of a relational dataset
    extra_data : preprocessing info
    info : original dataset informations

    Returns
    -------
    result : dictionary with corpus and relative infos
    """
    n = 0
    count = 0
    new_corpus = []
    new_labels = []
    new_edges = []
    compute_labels = len(labels) > 0
    compute_edges = 0 #len(edges) > 0
    words_mean = 0
    distinct_labels = {}
    for document in corpus:
        document_length = len(document)
        if document_length >= min_doc:
            words_mean += document_length
            new_corpus.append(document)
            if compute_labels:
                new_labels.append(labels[count])
                for label in labels[count]:
                    if label not in distinct_labels:
                        distinct_labels[label] = True
            if compute_edges:
                new_edges.append(edges[n])
            n += 1
        else:
            if n <= partition:
                partition -= 1
        count += 1
    words_document_mean = 0
    if n > 0:
        words_document_mean = round(words_mean/n, 2)

    vocabulary = get_vocabulary(new_corpus)

    train, test, y_train, y_test = train_test_split(range(len(new_corpus)), new_labels,
                                                    test_size=0.15,
                                                    random_state=1, stratify=new_labels)

    train, validation = train_test_split(train, test_size=3/17,
                                         random_state=1,
                                         stratify=y_train)

    partitioned_corpus = []
    partitioned_labels = []
    partitioned_edges = []

    for doc in train:
        partitioned_corpus.append(new_corpus[doc])
        partitioned_labels.append(new_labels[doc])
        #partitioned_edges.append(new_edges[doc])

    for doc in validation:
        partitioned_corpus.append(new_corpus[doc])
        partitioned_labels.append(new_labels[doc])
        #partitioned_edges.append(new_edges[doc])

    for doc in test:
        partitioned_corpus.append(new_corpus[doc])
        partitioned_labels.append(new_labels[doc])
        #partitioned_edges.append(new_edges[doc])


    extra_info = {}
    extra_info["total_documents"] = n
    extra_info["words_document_mean"] = words_document_mean

    extra_info["vocabulary_length"] = len(vocabulary)
    extra_info["last-training-doc"] = len(train)
    extra_info["last-validation-doc"] = len(validation)+len(train)

    extra_info["preprocessing-info"] = extra_data
    extra_info["info"] = info
    if compute_labels:
        extra_info["labels"] = list(distinct_labels.keys())
        extra_info["total_labels"] = len(extra_info["labels"])

    return Dataset(
        partitioned_corpus,
        vocabulary,
        extra_info,
        partitioned_labels,
        partitioned_edges)


def get_vocabulary(corpus):
    """
    Retrieve the vocabulary from the corpus

    Parameters
    ----------
    corpus : the corpus

    Returns
    -------
    vocabulary : dictionary of words
                 key = word
                 value = word/doc frequency, rounded to 4 decimals
    """
    corpus_length = len(corpus)
    vocabulary = {}
    for document in corpus:
        word_in_document = {}
        for word in document:
            if word in vocabulary:
                if not word in word_in_document:
                    word_in_document[word] = True
                    vocabulary[word] += 1
            else:
                word_in_document[word] = True
                vocabulary[word] = 1

    for word in vocabulary:
        vocabulary[word] = round(vocabulary[word]/corpus_length, 4)

    return vocabulary
