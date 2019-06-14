import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import numpy as np

df = pd.read_json('./timeslot_data.json')

#check data has been read in properly - 
print(df.head())
#check number of rows and columns in dataset - print(df.shape)

le = preprocessing.LabelEncoder()
timeslot_type_enc = le.fit_transform(df['timeslot_type'])
days_enc = df['days']
timeslot_enc = df['timeslot']
calendar_event_exist_enc = df['calendar_event_exist']
focus_enc = df['focus']

features = list(zip(days_enc, timeslot_enc, calendar_event_exist_enc))

X = features #df.drop(columns=['focus'])
y = df['focus'].values
#view target values - print(y[200:500])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)
## 7001 MON 7002 TUE 7003 WED 7004 THU 7005 FRI 7006 SAT 7007 SUN

knn_cv = KNeighborsClassifier(n_neighbors=1)
cv_scores = cross_val_score(knn_cv, X, y, cv=5)
print('cv_scores:{}'.format(cv_scores))
print('cv_scores mean:{}'.format(np.mean(cv_scores)))

knn2 = KNeighborsClassifier()
param_grid = {'n_neighbors': np.arange(1, 25)}
knn_gscv = GridSearchCV(knn2, param_grid, cv=5)
knn_gscv.fit(X, y)

print(knn_gscv.best_params_, knn_gscv.best_params_['n_neighbors'])
print(knn_gscv.best_score_)

# Create KNN classifier
knn = KNeighborsClassifier(n_neighbors = knn_gscv.best_params_['n_neighbors'])
knn.fit(X_train,y_train)

print('Predictions on test data:')
print((X_test)[0:10])
print(knn.predict(X_test)[0:10])

print('Predictions on manual input data:')
test = np.array([9000, 1635, 0])
test = test.reshape(1, -1)
print(knn.predict(test))

print('Prediction model accuracy:')
print(knn.score(X_test, y_test))