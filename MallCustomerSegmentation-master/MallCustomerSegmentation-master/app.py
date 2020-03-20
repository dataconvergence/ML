#step -1 # Importing flask module in the project is mandatory 
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import ipfsapi
#Step -2 Flask constructor takes the name of  
# current module (__name__) as argument.app = Flask(__name__)

app = Flask(__name__)

#Step -3 Load Trained  Model
model = pickle.load(open('Cluster.pkl', 'rb'))
def textfile(label):
    f= open("output.txt","w+")
    f.write(label)
    f.close() 

# Step -4 The route() function of the Flask class is a decorator,  
# which tells the application which URL should call  
# the associated function


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [float(x) for x in request.form.values()]
    c  = [np.array(int_features)]
    
    o = model.predict(c)
    if o == 4:
        Category = 'Sensible Clients'
    elif o == 3:
        Category = 'Careless Client'
    elif o == 2:
        Category = 'Target Client'
    elif o == 1:
        Category = 'Standard Client'
    else:
        Category = 'Careful Client'

    res=Category
    label="The Client belongs to "+str(res)+" Catergory"
    
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
   

    return render_template('index.html', prediction_text='The client belongs to {} Category'.format(Category),url1=url)

# main driver function
 # run() method of Flask class runs the application  
    # on the local development server.
if __name__ == "__main__":
    app.run(debug=False)

