Predicting Home Prices in Iowa 🏠
"""
## I. Wrangle Data

#Since real estate prices fluctuate over time, it's important to index the houses in this dataset using the year in which they were sold. 
#First, load the dataset into a DataFrame named `df` and find the column that states the year sold. 
#Next, modify the code below so that `Yr_Sold` column is parsed as a datetime object and set as the index.

"""
#Import data into DataFrame
import pandas as pd

url_train = 'https://drive.google.com/uc?export=download&id=1tmYLQ1RwIgjI_d66PWnlXU-5D_VxtiQc'
df = pd.read_csv(url_train)


def wrangle(filepath):
    df = pd.read_csv(filepath, parse_dates=['Yr_Sold'],
                     index_col='Yr_Sold')
    
    return df

filepath = url_train

df = wrangle(filepath)



#Create a scatter plot that shows `'SalePrice'` as a function of `'Gr_Liv_Area'`.

X=df[['Gr_Liv_Area']] 
y=df['SalePrice']

df['Gr_Liv_Area'].shape

import matplotlib.pyplot as plt

plt.figure(figsize=(15, 10))
plt.scatter(X, y)

plt.xlabel('Gr_Liv_Area')
plt.ylabel('SalePrice')
plt.legend();
"""
## II. Split Data

#Build a model to predict the price at which a house will be sold, thw target is the `'SalePrice'` column.
#Split `df` into `X` and `y`.
"""
target = 'SalePrice'
# YOUR CODE HERE
X = df.drop(columns=target)
y = df[target]


#Split `X` and `y` into training and validation sets. Since housing prices fluctuate over time, use the time-based cutoff method. 

cutoff = '2009'
mask = X.index < cutoff
X_train, y_train = X.loc[mask], y.loc[mask]
X_val, y_val = X.loc[~mask], y.loc[~mask]
"""
## III. Set Baseline

#Establish a baseline. Calculate the mean housing price for the training set. Calculate the *mean absolute error* for a model that always predicts that mean.
#Assign the mean absolute error to a variable named `baseline_mae`.

"""
from sklearn.metrics import mean_absolute_error

df['SalePrice_Mean'] = df['SalePrice'].mean()
baseline_mae = mean_absolute_error(df['SalePrice'],df['SalePrice_Mean'])
print('Baseline MAE:', baseline_mae)
"""
## IV. Build Models

#Build and train a linear regression model that predicts home sale price. Your model should have the following components:
"""
- A `OneHotEncoder` for categorical features.
- A `StandardScaler` so that you can compare your model coefficients after training.
- A `pipeline` that combines transformers and predictor.

from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from category_encoders import OneHotEncoder
from sklearn.preprocessing import StandardScaler


model_lr = make_pipeline(
    OneHotEncoder(use_cat_names=True),
    StandardScaler(),
    LinearRegression()
    )  

model_lr.fit(X_train, y_train);


#Build and train a ridge regression model that predicts home sales price. Your model should include the following components:

- A `OneHotEncoder` for categorical features.
- A `StandardScaler` so that you can compare your model coefficients after training.
- A `pipeline` that combines transformers and predictor.

from sklearn.linear_model import Ridge

model_r = make_pipeline(
    OneHotEncoder(use_cat_names=True),
    StandardScaler(),
    Ridge(normalize=False)
    )
    
model_r.fit(X_train, y_train);
"""
## V. Check Metrics

#Compare your models metrics by calculating their mean absolute error for the training and validation sets. 
#The validation MAE for your Ridge model should be lower than your `baseline_mae`.

"""
model_lr_training_mae = mean_absolute_error(y_train, model_lr.predict(X_train))
model_lr_validation_mae =  mean_absolute_error(y_val, model_lr.predict(X_val))

model_r_training_mae = mean_absolute_error(y_train, model_r.predict(X_train))
model_r_validation_mae = mean_absolute_error(y_val, model_r.predict(X_val))


print('Linear Regression Model')
print('Training MAE:', model_lr_training_mae)
print('Validation MAE:', model_lr_validation_mae)
print()
print('Ridge Regression Model')
print('Training MAE:', model_r_training_mae)
print('Validation MAE:', model_r_validation_mae)


#Compare your two models by calculating their $R^2$ score for the **validation data**

model_lr_r2_score = model_lr.score(X_val, y_val)
model_r_r2_score = model_r.score(X_val, y_val)
print('Linear Regression R^2:', model_lr_r2_score)
print('Ridge Regression R^2:', model_r_r2_score)

#Based on the metrics above, choose the best of the two models and generate an array of predictions.

url_test = 'https://drive.google.com/uc?export=download&id=1y9u8cOWprTjruw8E-ct1c7YaEytToqd_'
X_test = pd.read_csv(url_test)

def wrangle(filepath):
  df = pd.read_csv(filepath,
                   parse_dates = ['Yr_Sold'],
                   index_col = 'Yr_Sold')
  return df
X_test = wrangle(url_test)


y_pred = model_r.predict(X_test)
print('My predictions:', y_pred[:3])

## VI. Explain Model

#Create a horizontal barchart for your best performing model that shows the ten most important features for the model's predictions.

coefficients = model_r.named_steps['ridge'].coef_
features = model_lr.named_steps['onehotencoder'].get_feature_names()
feat_imp = pd.Series(coefficients, index=features).sort_values(key=abs)
feat_imp.tail(10).plot(kind='barh')
plt.xlabel('Coefficient [$]')
plt.ylabel('Feature')
plt.title('Coefficients for Ridge Regression');

feat_imp.tail(10).plot(kind='barh')
"""
