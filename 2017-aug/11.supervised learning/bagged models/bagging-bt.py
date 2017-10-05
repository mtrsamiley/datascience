import pandas as pd
import os
from sklearn import preprocessing
from sklearn import ensemble
from sklearn import tree
from sklearn import model_selection

#changes working directory
os.chdir("D:/titanic")

titanic_train = pd.read_csv("train.csv")
titanic_train.shape
titanic_train.info()

titanic_test = pd.read_csv('test.csv')
titanic_test.shape
titanic_test.info()
titanic_test.Survived = None

#it gives the same never of levels for all the categorical variables
titanic = pd.concat([titanic_train, titanic_test])

#create title column from name
def extract_title(name):
     return name.split(',')[1].split('.')[0].strip()
titanic['Title'] = titanic['Name'].map(extract_title)

#create an instance of Imputer class with required arguments
mean_imputer = preprocessing.Imputer()
#compute mean of age and fare respectively
mean_imputer.fit(titanic_train[['Age','Fare']])
#fill up the missing data with the computed means 
titanic[['Age','Fare']] = mean_imputer.transform(titanic[['Age','Fare']])

#creaate categorical age column from age
def convert_age(age):
    if(age >= 0 and age <= 10): 
        return 'Child'
    elif(age <= 25): 
        return 'Young'
    elif(age <= 50): 
        return 'Middle'
    else: 
        return 'Old'
titanic['Age1'] = titanic['Age'].map(convert_age)

titanic['FamilySize'] = titanic['SibSp'] +  titanic['Parch'] + 1
def convert_familysize(size):
    if(size == 1): 
        return 'Single'
    elif(size <=3): 
        return 'Small'
    elif(size <= 6): 
        return 'Medium'
    else: 
        return 'Large'
titanic['FamilySize1'] = titanic['FamilySize'].map(convert_familysize)

#convert categorical columns to one-hot encoded columns
titanic1 = pd.get_dummies(titanic, columns=['Sex','Pclass','Embarked', 'Age1', 'Title', 'FamilySize1'])
titanic1.shape
titanic1.info()

titanic2 = titanic1.drop(['PassengerId','Name','Age','Ticket','Cabin','Survived'], axis=1, inplace=False)
titanic2.shape

X_train = titanic2[0:titanic_train.shape[0]]
X_train.shape
X_train.info()
y_train = titanic_train['Survived']

#oob scrore is computed as part of model construction process
dt_estimator = tree.DecisionTreeClassifier()
bt_estimator = ensemble.BaggingClassifier(base_estimator= dt_estimator, oob_score=True, random_state=2017)
bt_grid = {'n_estimators':[3], 'base_estimator__max_depth':[3,4,5]}
grid_bt_estimator = model_selection.GridSearchCV(bt_estimator, bt_grid, cv=10,n_jobs=1)
grid_bt_estimator.fit(X_train, y_train)
print(grid_bt_estimator.grid_scores_)
print(grid_bt_estimator.best_score_)
print(grid_bt_estimator.best_params_)
print(grid_bt_estimator.score(X_train, y_train))

X_test = titanic2[titanic_train.shape[0]:]
X_test.shape
X_test.info()
titanic_test['Survived'] = grid_rf_estimator.predict(X_test)

titanic_test.to_csv('submission.csv', columns=['PassengerId','Survived'],index=False)
    
