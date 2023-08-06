# WRITTEN BY XAMPAK
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
from nltk import word_tokenize
from nltk import WordPunctTokenizer
from nltk import download
from nltk import TweetTokenizer
from nltk.corpus import stopwords
import string
from textblob import TextBlob
from textblob.sentiments import PatternAnalyzer
import datetime as datetime
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import mean_squared_error,r2_score,mean_absolute_error,max_error
download('stopwords')
download('punkt')
stop_words = set(stopwords.words("english"))


#looking

#creates a dataframe from a file path
def makeData(filepath):
    df = pd.read_csv(filepath)
    return df

# prints out quick statistical information
def showInfo(dataframe):
    print("Descriptive stats:\n\n")
    print(dataframe.describe())
    print("-"*50)
    print("Dataframe information:\n\n")
    print(dataframe.info())
    print("-"*50)
    print("Dataframe Head:\n\n")
    print(dataframe.head(5))


def numBarPlot(dataframe, items:list):
    def bar_plot(variable):
        """
            input: variable ex: "Sex"
            output: bar plot & value count
        """
        # get feature
        var = dataframe[variable]
        # count number of categorical variable
        varValue = var.value_counts()
        
        # visualize
        plt.figure(figsize = (9,3))
        plt.bar(varValue.index, varValue)
        plt.xticks(varValue.index, varValue.index.values)
        plt.ylabel("Frequency")
        plt.title(variable)
        plt.show()
        print("{}: \n {}".format(variable, varValue))

    for c in items:
        bar_plot(c)



def catPlots(dataframe,items:list):
    def plot_hist(variable):
        plt.figure(figsize = (9,3))
        plt.hist(dataframe[variable], bins = 50)
        plt.xlabel(variable)
        plt.ylabel("Frequency")
        plt.title("{} distrubution with hist".format(variable))
        plt.show()
    for n in items:
        plot_hist(n)


def countMissing(df):
    print(df.isnull().sum())

def modeFill(dataframe,colName):
    dataframe[colName] = dataframe[colName].fillna(dataframe[colName].mode()[0])
    return dataframe

def meanFill(dataframe,colName):
    dataframe[colName] = dataframe[colName].fillna(dataframe[colName].mean().round(3))
    return dataframe


def subSetDf(dataframe,col,value,condition):
    if condition == 'gte':
        df = df[df[col] >= value]
    elif condition == 'lte':
        df = df[df[col] <= value]
    elif condition == 'eq':
        df = df[df[col] == value]
    elif condition == 'gt':
        df = df[df[col] > value]
    elif condition == 'lt':
        df = df[df[col] < value]
    else:
        print(f'{condition} is not a valid selection, choose from the list: \n gt\nlt\gte\nlte\neq')

# dimension row or col
def dropnaDim(data,dimension):
    dimension = dimension.lower()
    if dimension =='row':
        data = data.dropna(axis=0)
    elif dimension == 'col':
        data = data.dropna(axis=1)
    else:
        print('Choose "row" or "col" for your dimension parameter on method of dropping.')
    return data

# takes all things where its not equal to this value        
def OutDF(df,col,val):
    df = df[df[col] != val]
    return df


def renameCols(df,remove,replace):
  df = df.rename(columns=lambda x: x.strip(remove))
  df = df.rename(columns=lambda x: x.replace(' ',replace))
  return df


def countUnique(df,col,n):
    if n == 0:
        print(df[col].value_counts(ascending=False,dropna=False))
    else:
        print(df[col].value_counts(ascending=False,dropna=False).head(n))

def dataTypeSplit(df):
    nums = []
    nonnums = []

    for i in df.columns:
      if df[i].dtypes == int or df[i].dtypes == float:
        nums.append(i)
      else:
        nonnums.append(i)

    numdf = df[nums]

    nonnumdf = df[nonnums]

    return numdf,nonnumdf

def groupedAVG(df,cols):
    return df.groupby(cols).mean()


def dropCol(df, col):
    return df.drop(col,axis=1)

# for seniment analysis on larger chunks of text, bigger than social 
# returns appended columns of comma sep subjectivity and polarity
def bigSenti(df,column):
    def Remove_Punctuation(tokenList):
        punctList = list(string.punctuation)
        punctList.remove("'")
        return [word for word in tokenList if word not in punctList]
    def Remove_Stop_Words(tokenList, stop_words):
        return [word for word in tokenList if word not in stop_words]
    def PreProcess(x):
        return Remove_Punctuation(Remove_Stop_Words(Tokenize(x),stop_words))
    def Tokenize(text):
        return TweetTokenizer().tokenize(str(text).lower())
    df = df[df[column].notnull()].copy()
    df[f'{column}_Tokenized'] = df[column].apply(lambda x: PreProcess(x))
    df[f'{column}_Sentiment'] = df[f'{column}_Tokenized'].apply(lambda x: list(TextBlob(" ".join(x), analyzer=PatternAnalyzer()).sentiment))
    
    for sentiment,index in zip(['polarity', 'subjectivity'],[0,1]):
        df[f'{column}_{sentiment}'] = df[f'{column}_Sentiment'].apply(lambda x: x[index])
        
    return df



# takes in a dataframe and a coiumn containing the text from social media sites
# returns the dataframe with more information than bigSenti and shows a compound overall score
def socialSentiment(df,col):
    #load VADER
    analyzer = SentimentIntensityAnalyzer()
    #Add VADER metrics to dataframe
    df['compound'] = [analyzer.polarity_scores(v)['compound'] for v in df[col]]
    df['neg'] = [analyzer.polarity_scores(v)['neg'] for v in df[col]]
    df['neu'] = [analyzer.polarity_scores(v)['neu'] for v in df[col]]
    df['pos'] = [analyzer.polarity_scores(v)['pos'] for v in df[col]]
    df.head(3)
    return df


# linear regression model quickly on numerical data!!
def linAlgo(df,target,test_size,random_state):
    X = df.drop(target,axis=1)
    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    regr = linear_model.LinearRegression()
    regr.fit(X_train, y_train)
    y_pred = regr.predict(X_test)


    labs = X_train.columns.tolist()
    coef = regr.coef_.squeeze().tolist()
    # Zip together
    labels_coef = list(zip(labs, coef))

    print('The feature and its respective coefficient: \n')
    # Verify the result
    for i in labels_coef:
        print(i)

    print('\nMean squared error: %.4f\n'
          % mean_squared_error(y_test, y_pred))
    # The coefficient of determination: 1 is perfect prediction
    print('\nCoefficient of determination: %.4f\n'
          % r2_score(y_test, y_pred))
    print('\nMean Absolute Error: %.4f\n'
      % mean_absolute_error(y_test,y_pred))
    print('\nMax Error: %.4f\n'
      % max_error(y_test,y_pred))

def KNN(df,cols,neighbors,targ,test_size):

    data_knn = df[cols]

    knn = KNeighborsClassifier(n_neighbors = neighbors)

    x,y = data_knn.loc[:,data_knn.columns != targ], data_knn.loc[:,targ]

    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = test_size, random_state = 42)

    knn.fit(x_train,y_train)
    prediction = knn.predict(x_test)

    print(f'With KNN (K={neighbors}) accuracy is: ', knn.score(x_test,y_test))



