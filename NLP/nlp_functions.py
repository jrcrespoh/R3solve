import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import argparse
import io
import json
import os

from google.cloud import language
import numpy
import six

# Use a service account
cred = credentials.Certificate('/Users/andyliu/develop/pennapps/NLP/pennapps-b49dc-f3f8ef18d574.json')
firebase_admin.initialize_app(cred)

#initialize database
db = firestore.client()

#users_ref = db.collection(u'users')
#docs = users_ref.stream()

def classify(text, verbose):
    """Classify the input text into categories. """

    language_client = language.LanguageServiceClient()

    document = language.types.Document(
        content=text,
        type=language.enums.Document.Type.PLAIN_TEXT)
    response = language_client.classify_text(document)
    categories = response.categories

    result = {}

    for category in categories:
        # Turn the categories into a dictionary of the form:
        # {category.name: category.confidence}, so that they can
        # be treated as a sparse vector.
        result[category.name] = category.confidence

    if verbose:
        print(text)
        for category in categories:
            print(u'=' * 20)
            print(u'{:<16}: {}'.format('category', category.name))
            print(u'{:<16}: {}'.format('confidence', category.confidence))

    return result

def addToIndex(data, index_file):
    with open(index_file, 'r') as f:
        d = json.load(f)['objects']
        d.append(data)
    with open(index_file, 'w') as f:
        d={"objects":d}
        json.dump(d,f)

def split_labels(categories):
    """The category labels are of the form "a-b-c" up to three levels,
    for example "/Computers & Electronics/Software", and these labels
    are used as keys in the categories dictionary, whose values are
    confidence scores.
    The split_labels function splits the keys into individual levels
    while duplicating the confidence score, which allows a natural
    boost in how we calculate similarity when more levels are in common.
    Example:
    If we have
    x = {"a/b/c": 0.5}
    y = {"a/b": 0.5}
    z = {"a": 0.5}
    Then x and y are considered more similar than y and z.
    """
    _categories = {}
    for name, confidence in six.iteritems(categories):
        labels = [label for label in name.split('/') if label]
        for label in labels:
            _categories[label] = confidence

    return _categories

def similarity(categories1, categories2):
    """Cosine similarity of the categories treated as sparse vectors."""
    categories1 = split_labels(categories1)
    categories2 = split_labels(categories2)

    norm1 = numpy.linalg.norm(list(categories1.values()))
    norm2 = numpy.linalg.norm(list(categories2.values()))

    # Return the smallest possible similarity if either categories is empty.
    if norm1 == 0 or norm2 == 0:
        return 0.0

    # Compute the cosine similarity.
    dot = 0.0
    for label, confidence in six.iteritems(categories1):
        dot += confidence * categories2.get(label, 0.0)

    return dot / (norm1 * norm2)

def query(index_file, text, n_top=3, verbose=False):
    """Find the indexed files that are the most similar to
    the query text.

    index_file is a filepath to a json file right now? 
    """
    similarities = []
    with open(index_file, 'r') as infile:
        index = json.load(infile)
    # Get the categories of the query text.
        query_categories = classify(text, verbose=False)

        #print(index)
        for obj in index['objects']:
            try:
                #print(obj)
                categories = obj['categories']
                #print((query_categories, categories))
                similarities.append((obj, similarity(query_categories, categories)))
            except AttributeError:
                #TODO: fix this
                pass

    similarities = sorted(similarities, key=lambda p: p[1], reverse=True)[:n_top]
    if verbose:
        print('=' * 20)
        print('Query: {}\n'.format(text))
        for category, confidence in six.iteritems(query_categories):
            print('\tCategory: {}, confidence: {}'.format(category, confidence))
        print('\nMost similar {} indexed texts:'.format(n_top))
        for filename, sim in similarities[:n_top]:
            print('\tFilename: {}'.format(filename))
            print('\tSimilarity: {}'.format(sim))
            print('\n')
    return similarities

