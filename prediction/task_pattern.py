import pandas as pd

from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

# reading the JSON data using json.load()
trainset = {
    "finished": ""
}
dict_train = json.load(train_file)

# converting json dataset from dictionary to dataframe
train = pd.DataFrame.from_dict(dict_train, orient='index')
train.reset_index(level=0, inplace=True)

df = pd.read_csv('./data_day.csv')
#check data has been read in properly - print(df.head())
#check number of rows and columns in dataset - print(df.shape)

X = df.drop(columns=['ActivityStatus'])
#check that the target variable has been removed - print(X.head())

y = df['ActivityStatus'].values
#view target values - print(y[0:5])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)
model = GaussianNB()
model.fit(X_train,y_train)

#show first 5 model predictions on the test data
print('Predictions on test data:')
print((X_test)[0:5])
print(model.predict(X_test)[0:5])

#manual input
import numpy as np
print('Predictions on manual input data:')
test = np.array([7002, 753, 0, 1001])
test = test.reshape(1, -1)
print(model.predict(test))

#check accuracy of our model on the test data
print('Prediction model accuracy:')
print(metrics.accuracy_score(y_test, model.predict(X_test)))

## 7001 MON 7002 TUE 7003 WED 7004 THU 7005 FRI 7006 SAT 7007 SUN