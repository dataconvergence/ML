#step -1 # Importing flask module in the project is mandatory 
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import ipfsapi
#Step -2 Flask constructor takes the name of  
# current module (__name__) as argument.app = Flask(__name__)

app = Flask(__name__)
def textfile(label):
    f= open("output.txt","w+")
    f.write(label)
    f.close()
#Step -3 Load Trained  Model
model = pickle.load(open('Product.pkl', 'rb'))

transform = pickle.load(open('Product_t.pkl', 'rb'))
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()

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
    c = transform.transform(c)
    result = model.predict(c)
    if result[0]==1:
        myresult="Purchased"
        
         
    else:
        myresult="Not Purchased"
        


    res=myresult
    label="The Customer "+str(res)+" the product."
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
   

    return render_template('index.html', prediction_text='The Customer {} the product '.format(res),url1=url)

# main driver function
 # run() method of Flask class runs the application  
    # on the local development server.
if __name__ == "__main__":
    app.run(debug=False)

