# cli tool to store files in firebase
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
import os
import sys
from sys import exit

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
    """
    Processes a filename to convert it to a format suitable for Firestore.

    Args:
        filename (str): The name of the file to process.

    Returns:
        str: The processed filename.
    """
    return filename

def filenameReverseProcessor(filename):
    # may be used in the future
    """
    Reverses the operation of filenameProccessor. This function is the inverse of filenameProccessor.

    Args:
        filename (str): The name of the file to reverse the operation on.

    Returns:
        str: The reversed filename.
    """
    return filename

def syncFromFirestore():
    """
    Downloads all files from Firestore and writes them into ./output.
    Each document in Firestore is expected to have a single field, 'content', which is a list of strings.
    The list of strings is written to a file in ./output as if it was a list of lines.
    If the Firestore collection is empty, the function raises a ConnectionError.
    """
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
    """
    Synchronizes the local output directory with Firestore.

    This function uploads files from the local './output' directory to the Firestore
    collection 'files'. If `skipDeletion` is False, it also checks for deleted files
    in the local directory and removes them from Firestore.

    Args:
        skipDeletion (bool): If True, skips deletion of files from Firestore that
                             are not present in the local './output' directory.
    """

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
    if len(sys.argv) < 2:
        print("==============================================")
        print("Usage: python3 database [download|upload]")
        print("Example: python3 database download")
        print("==============================================")
        raise ValueError("Expected 1 argument, got " + str(len(sys.argv) - 1))
        exit(1)
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
    