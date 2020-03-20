#Usage: python app.py
import os
 
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
import argparse
import time
import uuid
import base64
import os
import pandas as pd
import re
import numpy as np
import pickle
import keras
import ipfsapi
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Flatten, GlobalMaxPooling1D
from keras.layers.embeddings import Embedding
from keras.layers.core import Activation, Dropout, Dense
from keras.models import Sequential
from keras.layers import LSTM
from keras.models import Sequential, load_model,model_from_json
from tensorflow.keras import backend as K 


model_path = 'sarcasm.h5'


model_weights_path = 'sarcasmweights.h5'

one  = pickle.load(open('Tokenizer', 'rb'))


Tag_re = re.compile(r'<[^>]+>')

def preprocess_text(text):
    sen = remove_tags(text)
    sen = re.sub('[^a-zA-Z]', ' ', sen)
    sen = re.sub(r"\s+[a-zA-Z]\s+", ' ', sen)
    sen = re.sub(r'\s+', ' ', sen)
    return sen
def remove_tags(text):
    return Tag_re.sub('',text)
def textfile(label):
    f= open("output.txt","w+")
    f.write(label)
    f.close() 


app = Flask(__name__)

@app.route("/")
def template_test():
    return render_template('template.html', label='', imagesource='../uploads/template.jpg')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print("Upload")
        mytext = request.form['text']
        
        user=preprocess_text(mytext)
        user = one.texts_to_sequences(user)
        user = pad_sequences(user, maxlen=29, dtype='int32', value=0)
        model = load_model(model_path)
        model.load_weights(model_weights_path)
        sentiment = model.predict(user,batch_size=1,verbose = 2)[0]
    if(np.argmax(sentiment) == 0):
        
        sentiment = "Non-sarcastic"
   
       
    elif (np.argmax(sentiment) == 1):
        sentiment = "sarcasm"
        
    keras.backend.clear_session()
    try:
            api = ipfsapi.connect('127.0.0.1', 5001)
            print(api)
    except ipfsapi.exceptions.ConnectionError as ce:
            print(str(ce))
    textfile(sentiment)
    new_file = api.add("output.txt")
    hash=new_file['Hash']
    api.pin.add(hash) 
    url='https://ipfs.io/ipfs/'+hash
    print(url)
    return render_template('template.html',label=sentiment,url1=url )


if __name__ == "__main__":
    app.debug=False
    app.run(host='0.0.0.0', port=3000)
