#step -1 # Importing flask module in the project is mandatory 
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import ipfsapi
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
one = OneHotEncoder(sparse=False,handle_unknown='ignore')
#Step -2 Flask constructor takes the name of  
# current module (__name__) as argument.app = Flask(__name__)

app = Flask(__name__)

#Step -3 Load Trained  Model
model = pickle.load(open('titanic.pkl', 'rb'))
one  = pickle.load(open('titanic_t.pkl', 'rb'))

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
    #Data = (float(x) for x in request.form.values())
    Age=request.form['Age']
    Embarked=request.form['Embarked']
    Fare=request.form['Fare']
    Parch=request.form['Parch']
    Pclass=request.form['Pclass']
    Sex=request.form['Sex']
    siblings=request.form['siblings']
    Title=request.form['Title']
    Familysize=request.form['Familysize']
    
    
    Data={'Age':[Age],'Embarked':[Embarked],'Fare':[Fare],'Parch':[Parch],'Pclass':[Pclass],'Sex':[Sex],'siblings':[siblings],'Title':[Title],'familysize':[Familysize]}
   
    
    df1 = pd.DataFrame(Data)
   
    x = one.transform(df1)
    x = x[:,1:]
    print(x.shape)
    output = model.predict(x)
    if output[0] == 1:
        passenger = 'Survived'
    else:
        passenger = 'Not Survived'
    res = passenger
    label="Passenger status : "+str(res)
    
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

    
    return render_template('index.html', prediction_text=' Passenger Status: {}'.format(res),url1=url)


# main driver function
 # run() method of Flask class runs the application  
    # on the local development server.
if __name__ == "__main__":
    app.run(debug=True)

