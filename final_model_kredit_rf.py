# -*- coding: utf-8 -*-
"""Final_Model_Kredit_RF.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VTtoaG7lXqlEgSRT8uZS1x7Y4I3IOavO
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns

from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, KFold, GridSearchCV, cross_val_score
from sklearn.feature_selection import chi2, RFE

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score, classification_report, explained_variance_score, plot_confusion_matrix
from sklearn.metrics import classification_report, confusion_matrix

from sklearn_pandas import DataFrameMapper
from sklearn.pipeline import Pipeline

from pickle import dump
from pickle import load

import warnings
warnings.filterwarnings('ignore')

msh_data = pd.read_csv('DataAlternatif.csv')
msh_data.head(10)

# Checking the size of dataset
msh_data.shape

#Summarizing the overall dataset
msh_data.info()

#Checking the null values in dataset
msh_data.isnull().sum()

#Checking the duplicate values
msh_data.duplicated().sum()

#Statistical description of data
msh_data.describe(include='O')

#Checking the unique values in each column
col = msh_data.columns

for i in col:
    uqv = msh_data[i].unique()
    print(i, ':', uqv,'\n')

#Count of the unique values in each columns
col = msh_data.columns

for i in col:
    c_uqv = msh_data.value_counts(i)
    print(c_uqv,'\n' '\n')

#Visualising the count of mushroom class
plt.figure(figsize=(8,5))
ax = sns.countplot(x = msh_data['Status'])
plt.title('Count of Data Alternatif')
plt.show()

data = msh_data.copy()

data.Status=data.Status.map({'Aproved':1,'Reject':0})
data.Status.value_counts()

data.Character=data.Character.map({'Percaya':2,'Normal':1,'Tidak':0})
data.Character.value_counts()

data.Capacity=data.Capacity.map({'Mampu':2,'Sedang':1,'Tidak':0})
data.Capacity.value_counts()

data.Capital=data.Capital.map({'Baik':2,'Sedang':1,'Tidak':0})
data.Capital.value_counts()

data.Condition=data.Condition.map({'Baik':2,'Normal':1,'Tidak':0})
data.Condition.value_counts()

data.Collateral=data.Collateral.map({'Kuat':2,'Sedang':1,'Tidak':0})
data.Collateral.value_counts()

data.isnull().sum()

data.info()

data.head(10)

#Splitting the variables into features & target
X = data.iloc[:, 1:]
y = data[['Status']]

#Segregating data into train & test
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, test_size=0.2, shuffle=True)

rfc = RandomForestClassifier(n_estimators=10, criterion='gini', max_depth=5, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='sqrt', max_leaf_nodes=None, min_impurity_decrease=0.0, bootstrap=True, oob_score=False, n_jobs=None, random_state=None, verbose=0, warm_start=False, class_weight=None, ccp_alpha=0.0, max_samples=None)

# Fit RandomForestClassifier
rfc.fit(X_train, y_train)
# Predict the test set labels
y_pred = rfc.predict(X_test)

#Testing the accuracy for all models
cc  = [y_pred]
mod = ['Random Forest']

print('Accuracy Scores for all models','\n')

for i,j in zip(cc, mod):
    print('==========================')
    print(j, ':', accuracy_score(y_test, i).round(2))
    print('==========================', '\n')

rfc.predict(X_test)

from sklearn.metrics import accuracy_score,precision_score,recall_score,confusion_matrix,classification_report, ConfusionMatrixDisplay
accuracy_train_rf = rfc.score(X_train, y_train)
accuracy_test_rf  = rfc.score(X_test, y_test)

print(f"Akurasi Model (Train) : {np.round(accuracy_train_rf * 100,2)} %")
print(f"Akurasi Model (Test)  : {np.round(accuracy_test_rf * 100,2)} %")

# Import `tree` module
from sklearn import tree

features = X.columns.values # The name of each column
classes = ['A','C'] # The name of each class
# You can also use low, medium and high risks in the same order instead
# classes = ['low risk', 'medium risk', 'high risk']

for estimator in rfc.estimators_:
    plt.figure(figsize=(12,6))
    tree.plot_tree(estimator,
                   feature_names=features,
                   class_names=classes,
                   fontsize=8, 
                   filled=True, 
                   rounded=True)
    plt.show()

cm = confusion_matrix(y_test, y_pred)

x_axis_labels = ["A", "C"]
y_axis_labels = ["A", "C"]

f, ax = plt.subplots(figsize =(7,7))
sns.heatmap(cm, annot = True, linewidths=0.2, linecolor="black", fmt = ".0f", ax=ax, cmap="Purples", xticklabels=x_axis_labels, yticklabels=y_axis_labels)
plt.xlabel("PREDICTED LABEL")
plt.ylabel("TRUE LABEL")
plt.title('Confusion Matrix for Random Forest Classifier');
#plt.savefig("rfcm.png", format='png', dpi=900, bbox_inches='tight')
plt.show()

cc  = [y_pred]
mod = ['Random Forest']

print('Classification Report for all models','\n')

for i,j in zip(cc, mod):
    print('========================================================')
    print(j,'\n\n' , classification_report(y_test, i))
    print('========================================================', '\n')

#Correlation Analysis in tabular form
data.corr().round(2)

##Correlation Analysis in visual form
plt.figure(figsize=(14,8))
sns.heatmap(data.corr().round(2), annot=True)
plt.title('Correlation between variables')
plt.show()

#Analysis of correlation between target & feature variables 
data.corr()['Status'].sort_values().round(2)

#Using the mapper to perform specific transformer to the features
m = DataFrameMapper([(['Character', LabelEncoder()]), (['Capacity', LabelEncoder()]), (['Capital', LabelEncoder()]),
                     (['Condition', LabelEncoder()]), (['Collateral', LabelEncoder()])])

#Making the pipeline stepwise
model = Pipeline(steps=[('mapper', m), ('mod', rfc)])
model

data

uid = msh_data.loc[:, ['Character', 'Capacity', 'Capital', 'Condition', 'Collateral','Status']]

#Picking up 10 random samples from our original data
ref = uid.sample(n=10, random_state=1)
ref

#Splititing the collected samples for testing 
uid_Xtest = ref.iloc[:, :-1]
uid_ytest = ref[['Status']]

data2 = uid.copy()
data2.shape

data2

#Splitting the original data for training the model
X_t = data2.iloc[:, :-1]
y_t = data2[['Status']]

data2['Character']

y_t

#Training the model
model.fit(X_t, y_t)

#Model Testing & Evaluation

print('Actual data:', '   ',uid_ytest.values.flatten(), '\n')

print('Predicted data: ', model.predict(uid_Xtest))

#Saving the model to file
dump(model, open('Kredit.pkl', 'wb'))

#Loading the file
ml = load(open('Kredit.pkl', 'rb'))

#Running the file for testing & evaluating 
print('Predicted Values:', ml.predict(uid_Xtest))