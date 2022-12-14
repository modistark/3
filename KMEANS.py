# -*- coding: utf-8 -*-
"""KMeans01.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16SminSxPgS4tnRYYz8-k-ygC7OqG-ey8

importing libraries
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import zipfile
import cv2
import plotly.express as px

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

"""Reading dataset"""

df = pd.read_csv('/content/sales_data_sample.csv', encoding = 'unicode_escape', parse_dates=['ORDERDATE'])

"""Data Preprocessing"""

df.dtypes

df.info()

df.isna().sum()

df.columns

df_drop = ['CUSTOMERNAME', 'PHONE', 'ORDERNUMBER',
       'ADDRESSLINE1', 'ADDRESSLINE2', 'CITY', 'STATE', 'POSTALCODE', 'TERRITORY', 'CONTACTLASTNAME', 'CONTACTFIRSTNAME',]
df = df.drop(df_drop, axis = 1)
df.head()

df.shape

df.isna().sum()

"""Data visualization"""

def Visualization(x):
  fig = plt.Figure(figsize = (12,6))
  fig = px.bar(x = df[x].value_counts().index, y = df[x].value_counts(), color = df[x].value_counts().index, height = 600)
  fig.show();

Visualization('COUNTRY')

Visualization('STATUS');

#DROP UNBALANCED FEATURE
df.drop(columns = ['STATUS'], axis = 1, inplace = True)
print('Columns resume:',df.shape[1])

Visualization('PRODUCTLINE')

Visualization('DEALSIZE')

#PREPARE DATA

def dummies(x):
  dummy = pd.get_dummies(df[x])
  df.drop(columns = x, inplace = True)
  return pd.concat([df,dummy], axis = 1)

df = dummies('COUNTRY')
df = dummies('PRODUCTLINE')
df = dummies('DEALSIZE')

df.head()

df.head()

y = pd.Categorical(df['PRODUCTCODE'])
y

df['PRODUCTCODE'] = pd.Categorical(df['PRODUCTCODE']).codes
df.head()

df_group = df.groupby(by = 'ORDERDATE').sum()
fig = px.line(x = df_group.index, y = df_group.SALES, title = 'sales_peak')
fig.show();

df.drop('ORDERDATE', axis = 1, inplace = True)

df.drop('QTR_ID', axis = 1, inplace = True)

df.shape

from sklearn.preprocessing import StandardScaler, normalize
from sklearn.cluster import KMeans

scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

scores = []
range_values = range(1,15)
for i in range_values:
  kmeans = KMeans(n_clusters = i)
  kmeans.fit(df_scaled)
  scores.append(kmeans.inertia_)

plt.plot(scores, 'bx-')
plt.title('finding right number of clustrs')
plt.xlabel('Clusters')
plt.ylabel('scores')
plt.show();

#the elbow method

kmeans = KMeans(4)
kmeans.fit(df_scaled)

labels = kmeans.labels_
labels

kmeans.cluster_centers_.shape

cluster_centers = pd.DataFrame(data = kmeans.cluster_centers_, columns= [df.columns])

cluster_centers

#invert the data
cluster_centers = scaler.inverse_transform(cluster_centers)
cluster_centers = pd.DataFrame(data = cluster_centers, columns = [df.columns])
cluster_centers

sales_of_cluster = pd.concat([df, pd.DataFrame({'cluster': labels})], axis = 1)
sales_of_cluster.head()