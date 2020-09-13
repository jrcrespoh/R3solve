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

cred = credentials.Certificate('/Users/andyliu/develop/pennapps/NLP/pennapps-b49dc-f3f8ef18d574.json')
firebase_admin.initialize_app(cred)
#initialize database
db = firestore.client()
categories = []
with open('./categories.txt', 'r') as f:
    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip('\n').replace('/', '-')[1:]
        categories.append(line)
#print(categories)

for cat in categories:
    data = {
    u'count': 0,
    u'name': cat,
    u'problems': [],
    }
    db.collection(u'categories').document(cat).set(data)
