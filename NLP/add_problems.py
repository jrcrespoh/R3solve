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
from nlp_functions import *

index_file = 'problems.json'

cred = credentials.Certificate('/Users/andyliu/develop/pennapps/NLP/pennapps-b49dc-f3f8ef18d574.json')
#firebase_admin.initialize_app(cred)
#initialize database
db = firestore.client()

def update(text, index_file):
    #given text, posts problem containing text
    classification = classify(text, verbose=False)
    #print(classification)
    data = {
    u'categories':classification, 
    u'display':text,
    u'followers':[],
    u'satisfied':0,
    u'solutions':[],
    u'timestamp':0, #TODO: figure out later
    u'upvotes':1,
    }
    addToIndex(data, index_file)

    similarValues = query(index_file, text, n_top = 3, verbose = False)
    print(similarValues)
    #TODO: display similarValues somehow, this is a JavaScript problem
    db.collection(u'problems').add(data)

#testing
problems = []
with open('./problems.txt', 'r') as f:
    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip('\n').replace('/', '-')
        problems.append(line)
#print(problems)

for problem in problems:
    update(problem, index_file)