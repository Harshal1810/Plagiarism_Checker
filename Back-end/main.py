from typing import Union, List
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache
from tempfile import NamedTemporaryFile
import tensorflow_hub as hub
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import string
#import nltk


app = FastAPI()

origins=[
  "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    
    # Remove punctuation and special characters
    text = text.translate(str.maketrans("", "", string.punctuation))
    
    return text
# Load the Universal Sentence Encoder
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

# Create a TfidfVectorizer instance
vectorizer = TfidfVectorizer()

@app.post('/plag_checker')
def plag_checker(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    # Create temporary files to save uploaded content
    with NamedTemporaryFile(delete=False) as temp_file1, NamedTemporaryFile(delete=False) as temp_file2:
        temp_file1.write(file1.file.read())
        temp_file2.write(file2.file.read())
        temp_file1_path = temp_file1.name
        temp_file2_path = temp_file2.name

    # Read the content of the temporary files
    with open(temp_file1_path, "r") as f1, open(temp_file2_path, "r") as f2:
        text1 = f1.read()
        text2 = f2.read()

    # Delete temporary files
    import os
    os.unlink(temp_file1_path)
    os.unlink(temp_file2_path)

    text1 = preprocess_text(text1)
    text2 = preprocess_text(text2)

    # Calculate sentence embeddings
    embeddings = embed([text1, text2])
    cosine_sim_semantic = cosine_similarity([embeddings[0]], [embeddings[1]])

    # Create a TfidfVectorizer instance
    vectorizer = TfidfVectorizer()

    # Fit and transform the text documents
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    # Calculate cosine similarity between the documents
    cosine_sim_tfidf = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
 
    print(text1, text2)
    ans1 = round(cosine_sim_tfidf[0][0]*100,4)
    ans2 = round(cosine_sim_semantic[0][0]*100,4)
    ans =   {'tfif':str(ans1) +"%",'semantic': str(ans2)+"%"}
    print(ans)
    return ans
    