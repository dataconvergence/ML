import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from sklearn.preprocessing import PolynomialFeatures
import ipfsapi

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
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
    data =request.form['msg']
    data=float(data)
    #int_features = (float(x) for x in request.form.values())
    final_features = np.array(data)
    poly = PolynomialFeatures(degree = 5)
    prediction = poly.fit_transform(final_features.reshape(-1,1))

    prediction = model.predict(prediction)
    label="Water Temperature should be degrees "+str(prediction)
    
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
    

    #output = round(prediction[0], 2)

    return render_template('index.html', prediction_text='Water Temperature should be degrees {}'.format(prediction),url1=url)




if __name__ == "__main__":
    app.run(debug=True)
