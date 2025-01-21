# cli tool to store files in firebase
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
import os
import sys
from sys import exit

if len(sys.argv) < 2:
    print("==============================================")
    print("Usage: python3 database [download|upload]")
    print("Example: python3 database download")
    print("==============================================")
    raise ValueError("Expected 1 argument, got " + str(len(sys.argv) - 1))
    exit(1)

README = ["# Hello World", "## This is saved in firestore", "### get scammed google ahahahahaha", "If you see this, you initialized the database, and you can now edit the files in ./output.", "", "If this isn't your first time, the directory on firebase was empty"]

# go through README and append an \n on each line
README = [line + '\n' for line in README]

cred = credentials.Certificate("./ServiceAccountKey.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client()
doc_ref = store.collection(u'files')
os.makedirs('./output', exist_ok=True)

def filenameProccessor(filename):
    # may be used in the future
    return filename

def filenameReverseProcessor(filename):
    # may be used in the future
    return filename

def syncFromFirestore():
    try:
        # Write files into ./output
        # {'content': ['print("Hello World")']}
        docs = doc_ref.get()
        for doc in docs:
            file = open('./output/' + filenameReverseProcessor(doc.id), 'w')
            # loop over lines
            file.writelines(doc.to_dict()['content'])
            file.close()
    except google.cloud.exceptions.NotFound:
        raise ConnectionError("Missing files in firestore")

def syncToFirestore(skipDeletion: bool = False):
    # loop through the firestore version to check for changes
    if not skipDeletion:
        for doc in doc_ref.get():
            # check if file exists in the output folder
            if os.path.exists('./output/' + filenameReverseProcessor(doc.id)):
                # Path exists, nothing to do
                pass
            else:
                # THE FILE WAS DELETED
                store.document("files/" + doc.id).delete()

    # loop over every file in ./output
    for filename in os.listdir('./output'):
        file = open('./output/' + filenameProccessor(filename), 'r')
        content = file.readlines()
        file.close()
        doc_ref.document(filename).set({'content': content})

if __name__ == '__main__':
    count = 0

    docs = doc_ref.stream()
    for doc in docs:
        count += 1

    if count == 0:
        doc_ref.document(filenameProccessor("README.md")).set({'content': README})
        syncFromFirestore()
        exit(0)
    if sys.argv[1] == 'download':
        syncFromFirestore()
    elif sys.argv[1] == 'upload':
        syncToFirestore(False)
    