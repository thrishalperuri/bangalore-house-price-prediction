import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df1=pd.read_csv("Bengaluru_House_Data.csv")
#print(df1.head())
#print(df1.shape)
print(df1.groupby('area_type')['area_type'].agg('count'))
df2=df1.drop(['area_type','availability','society','balcony'],axis='columns')
# print(df2.head())
print(df2.isnull().sum())
df3=df2.dropna()
print(df3)
print(df3['size'].unique())
df3['bhk']=df3['size'].apply(lambda x: int(x.split(' ')[0]))
print(df3.head())
print(df3['bhk'].unique())
print(df3[df3.bhk>20])
print(df3['total_sqft'].unique())#so here found some sq ft that are in range"-" for that case we are trying to covert em to float , if it aint possible we are returining bool False

def is_float(x):
    try:
        float(x)
    except:
        return False
    return True
print(df3[~df3['total_sqft'].apply(is_float)].head())#we can see an operator"~" its a NOT operator that gives opp of a bool
def sqft_to_num(x):#this mini function we are creating is essential for convertion
    tokens=x.split('-')
    if len(tokens)==2:
        return (float(tokens[0])+float(tokens[1]))/2
    try:
        return float(x)
    except:
        return None
df4=df3.copy()
df4['total_sqft']=df4['total_sqft'].apply(sqft_to_num)
print(df4.head())
print(df4.loc[30])
df5=df4.copy()
df5['price_per_sqft']=df5['price']*100000/df5['total_sqft']
df5.head()
print(len(df5.location.unique()))
df5.location=df5.location.apply(lambda x : x.strip())#here we use strip function, because we need remove the extra space for each strings
#we are counting the locations individually
loc_Stats=df5.groupby('location')['location'].agg('count')
print(loc_Stats)
loc_less_than_10=loc_Stats[loc_Stats<=10]#so here we are filtering the locations, where they are repeated only once
df5.location=df5.location.apply(lambda x:"other" if x in loc_less_than_10 else x)
print(len(df5.location.unique()))
print(df5[df5.total_sqft/df5.bhk<300].head())#obtaining values that are irrrelavent/abmormal
df6=df5[~(df5.total_sqft/df5.bhk<300)]#we are creating a df, where we will have the values after removal of abnormal ones
print(df6.head())
print(df6.shape)
def remove_pps_outliers(df):

    df_out = pd.DataFrame()

    for key, subdf in df.groupby('location'):

        m = np.mean(subdf.price_per_sqft)

        st = np.std(subdf.price_per_sqft)

        reduced_df = subdf[
            (subdf.price_per_sqft > (m-st))
            &
            (subdf.price_per_sqft <= (m+st))
        ]

        df_out = pd.concat([df_out, reduced_df], ignore_index=True)

    return df_out
df7=remove_pps_outliers(df6)
print(df7.shape)
#visualization
def plot_scatter_chart(df,location):
    bhk2=df[(df.location==location)&(df.bhk==2)]
    bhk3=df[(df.location==location)&(df.bhk==3)]
    plt.scatter(bhk2.total_sqft,bhk2.price,color='blue',marker='+',label='2 BHK',s=50)
    plt.scatter(bhk3.total_sqft,bhk3.price,color='green',marker='.',label='3 BHK',s=50)
    plt.xlabel('Total Square feet area')
    plt.ylabel('Total Square feet area')
    plt.title(location)
    plt.legend()
    #plt.show()
plot_scatter_chart(df7,'Rajaji Nagar')

def remove_bhk_outliers(df):

    exclude_indices = np.array([])

    for location, location_df in df.groupby('location'):

        bhk_stats = {}

        for bhk, bhk_df in location_df.groupby('bhk'):

            bhk_stats[bhk] = {
                'mean': np.mean(bhk_df.price_per_sqft),
                'std': np.std(bhk_df.price_per_sqft),
                'count': bhk_df.shape[0]
            }

        for bhk, bhk_df in location_df.groupby('bhk'):

            stats = bhk_stats.get(bhk - 1)

            if stats and stats['count'] > 5:

                exclude_indices = np.append(
                    exclude_indices,

                    bhk_df[
                        bhk_df.price_per_sqft < stats['mean']
                    ].index.values
                )

    return df.drop(exclude_indices, axis='index')
df8=remove_bhk_outliers(df7)
print(df8.shape)
df9 = df8[~(df8.bath > df8.bhk + 2)]
df10=df9.drop(['size','price_per_sqft'],axis='columns')
print(df10.head())
print(df10.shape)
dummies=pd.get_dummies(df10.location)
df11=pd.concat([df10,dummies.drop('other',axis="columns")],axis="columns")
print(df11.head(3))
df12=df11.drop('location',axis="columns")
X=df12.drop("price",axis="columns")
Y=df12.price
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.2,random_state=10)
from sklearn.linear_model import LinearRegression
Lr=LinearRegression()
Lr.fit(X_train,y_train)
print(Lr.score(X_test,y_test))
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
cv=ShuffleSplit(n_splits=5,test_size=0.2,random_state=0)
ex=cross_val_score(LinearRegression(),X,Y,cv=cv)
print(ex)
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV, ShuffleSplit
import pandas as pd

def find_best_model_using_gridsearchcv(X, y):

    algos = {

        'linear_regression': {
            'model': LinearRegression(),
            'params': {}
        },

        'lasso': {
            'model': Lasso(),
            'params': {
                'alpha': [1, 2, 5, 10],
                'selection': ['random', 'cyclic']
            }
        },

        'decision_tree': {
            'model': DecisionTreeRegressor(),
            'params': {
                'criterion': ['squared_error', 'friedman_mse'],
                'splitter': ['best', 'random']
            }
        }

    }

    scores = []

    cv = ShuffleSplit(
        n_splits=5,
        test_size=0.2,
        random_state=0
    )

    for algo_name, config in algos.items():

        gs = GridSearchCV(
            estimator=config['model'],
            param_grid=config['params'],
            cv=cv,
            return_train_score=False
        )

        gs.fit(X, y)

        scores.append({
            'model': algo_name,
            'best_score': gs.best_score_,
            'best_params': gs.best_params_
        })

    return pd.DataFrame(scores, columns=['model', 'best_score', 'best_params'])
RESULT=find_best_model_using_gridsearchcv(X,Y)
print(RESULT)
def predict_price(location, sqft, bath, bhk):

    # Find the column index of the location
    loc_index = np.where(X.columns == location)[0][0]

    # Create an input vector of all zeros
    x = np.zeros(len(X.columns))

    # Fill numerical features
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    # Set the selected location column to 1 (one-hot encoding)
    if loc_index >= 0:
        x[loc_index] = 1

    # Predict and return the house price
    return Lr.predict([x])[0]
print(X.columns)
print( '1st Phase JP Nagar',1000,2,2)
import pickle
with open("real_estate_price_prediction.pickle",'wb') as f:
    pickle.dump(Lr,f)
import json

columns = {
    'data_columns': [col.lower() for col in X.columns]
}

with open("columns.json", "w") as e:
    e.write(json.dumps(columns))