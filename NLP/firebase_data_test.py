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
categories = db.collection(u'categories').get()
for c in categories:
    print(c.to_dict())