# cli tool to store files in firebase
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
import os
import sys

cred = credentials.Certificate("./ServiceAccountKey.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client()
doc_ref = store.collection(u'files')

def syncFromFirestore():
    try:
        # Write files into ./output
        # {'content': ['print("Hello World")']}
        docs = doc_ref.get()
        for doc in docs:
            file = open('./output/' + doc.id, 'w')
            # loop over lines
            file.writelines(doc.to_dict()['content'])
            file.close()
    except google.cloud.exceptions.NotFound:
        print(u'Missing data')

def syncToFirestore():
    # loop over every file in ./output
    for filename in os.listdir('./output'):
        file = open('./output/' + filename, 'r')
        content = file.readlines()
        file.close()
        doc_ref.document(filename).set({'content': content})

if __name__ == '__main__':
    if sys.argv[1] == 'download':
        syncFromFirestore()
    elif sys.argv[1] == 'upload':
        syncToFirestore()