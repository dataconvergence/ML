#step -1 # Importing flask module in the project is mandatory 
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import ipfsapi
#Step -2 Flask constructor takes the name of  
# current module (__name__) as argument.app = Flask(__name__)

app = Flask(__name__)

#Step -3 Load Trained  Model
model = pickle.load(open('Randomforest.pkl', 'rb'))

# Step -4 The route() function of the Flask class is a decorator,  
# which tells the application which URL should call  
# the associated function
def textfile(label):
    f= open("output.txt","w+")
    f.write(label)
    f.close() 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)
    label="The House Price is "+str(output)
    
    try:
        api = ipfsapi.connect('127.0.0.1', 5001)
        print(api)
    except ipfsapi.exceptions.ConnectionError as ce:
        print(str(ce))
    textfile(label)
    new_file = api.add("output.txt")
    hash=new_file['Hash']
    api.pin.add(hash) 
    url='https://ipfs.io/ipfs/'+hash
    print(url)
    return render_template('index.html', prediction_text='House Price  {} K $'.format(output),url1=url)

# main driver function
 # run() method of Flask class runs the application  
    # on the local development server.
if __name__ == "__main__":
    app.run(debug=False)

