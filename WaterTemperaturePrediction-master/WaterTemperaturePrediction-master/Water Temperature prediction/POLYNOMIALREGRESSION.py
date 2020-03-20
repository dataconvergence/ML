#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[2]:


import pandas as pd


# In[3]:


import matplotlib.pyplot as plt


# In[4]:


Dataset = pd.read_csv(r"C:/Users/User/bottle.csv")


# In[5]:


Dataset.head()


# In[6]:


Dataset = Dataset[["Salnty","T_degC"]]
Dataset.cloumns=["Salinity","Temperature"]
Data = Dataset


# In[7]:


Dataset = Dataset[:][:500]


# In[8]:


import seaborn as sns
sns.lmplot(x="Salnty",y="T_degC",data = Dataset,order=2,ci=None);


# In[9]:


Dataset.isnull().sum()


# In[10]:


Dataset.fillna(method="ffill",inplace=True)


# In[11]:


Dataset.isnull().sum()


# In[12]:


x = np.array(Dataset["Salnty"]).reshape(-1,1)
y = np.array(Dataset["T_degC"]).reshape(-1,1)


# In[13]:


from sklearn.model_selection import train_test_split
X_train, X_test,y_train,y_test = train_test_split(x,y,test_size = 0.25)


# In[14]:


from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree = 5)
x_poly = poly.fit_transform(X_train)


# In[15]:


poly.fit(x_poly,y_train)


# In[16]:


from sklearn.linear_model import LinearRegression
lin = LinearRegression()
lin.fit(x_poly,y_train)


# In[17]:


x_poly1 = poly.fit_transform(X_test)


# In[18]:


y = lin.predict(x_poly1)


# In[19]:


df = pd.DataFrame(X_test)
df["predictions"] = y
df["Actual predictions"] = y_test


# In[20]:


df


# In[21]:


from sklearn.metrics import mean_squared_error,r2_score
print(np.sqrt(mean_squared_error(y_test,y)))
print(r2_score(y_test,y))


# In[23]:


import pickle
pkl_filename = "Temp.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(lin, file)


# In[ ]:




