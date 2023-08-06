import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sklearn
from matplotlib import colors
from sklearn import datasets
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os


def get_base_path():
    token = "\\src\\"
    curdir_path = os.path.abspath(os.curdir)
    PATH_BASE = curdir_path.partition(token)[0]
    separator = curdir_path.partition(token)[1]
    if separator==token:
        return  PATH_BASE
    else:
        return curdir_path




def nan_df(X=None):
    plt.figure(figsize = (16,5))
    sns.heatmap(X.isnull(), cbar=False)

# Codifica todas las variables categoricas o de tipo object con LabelEncoder
def encoder_cat(X=None,columns_cat=[]):    
    le = LabelEncoder()
    for c in columns_cat:
        col_type = X[c].dtype
        if col_type == 'object' or col_type.name == 'category':
            #print("column : "+str(c))
            X[c] = le.fit_transform(X[c])

def columns_cat(X):    
    _cols = X.columns
    _num_cols = X._get_numeric_data().columns
    _categorical_columns_name = list(set(_cols) - set(_num_cols))
    return _categorical_columns_name

def two_d(array):    
    np_array = np.array(array)    
    if(np_array.ndim==1):
        np_array=np_array.reshape(len(np_array),1)
    return np_array

# Generate dataset with 1000 samples, 100 features and 2 classes
def gen_dataset(n_samples=10000, n_features=100, n_classes=2, random_state=42,df=False):  
    X, y = datasets.make_classification(
        n_features=n_features,
        n_samples=n_samples,  
        n_informative=int(0.6 * n_features),    # the number of informative features
        n_redundant=int(0.0 * n_features),      # the number of redundant features
        n_repeated=int(0.0 * n_features), # the number of repeated features
        n_classes=n_classes, 
        random_state=random_state)
    
    if(df==True):
        df=pd.DataFrame(data=X[0:,0:],  index=[i for i in range(X.shape[0])],
                columns=['f'+str(i) for i in range(X.shape[1])])
        return (df, y)
    else:
        return (X, y)   
    
    
def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=-1, train_sizes=np.linspace(.1, 1.0, 7), score="",url_dir=""):
    """Generate a simple plot of the test and training learning curve"""
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score : "+score)
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes, scoring = score)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    if not url_dir:
        plt.show()
    else:
        plt.savefig(url_dir+'learning_curve.png', bbox_inches='tight')
        plt.close()
        


def pivot_columns(df_prod_bco_pivot):
    cls_fre = zip(df_prod_bco_pivot.columns.get_level_values(0),df_prod_bco_pivot.columns.get_level_values(1))
    simple_columns = []
    for i in cls_fre: 
        simple_columns.append(str(i[0])+"_"+str(i[1]))

    df_prod_bco_pivot.columns = simple_columns
    df_prod_bco_pivot.reset_index(inplace=True)
    #return simple_columns


def show_na(df):
    total = len(df)
    lista_nan_column = []
    for column in df.columns:
        total_na = df[column].isna().sum()
        per = total_na/total
        if(total_na>0):
            print(column+" : "+str(total_na)+ ", frac: "+str(total_na)+"/"+str(total) +" , per: "+str(per))
            lista_nan_column.append(column)
    return lista_nan_column

def clean_df(df, columns):
    for column in columns:
        df[column] = df[column].astype('str')
        df[column] = df[column].str.strip()
        df[column] = df[column].str.upper()
        

def plot_boundaries_iris_dataset(model, iris):
    plt.figure(figsize=(14, 8))
    for pairidx, pair in enumerate([[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]):
        
        
        # Parameters
        n_classes = 3
        plot_colors = "rgb"
        cmap = colors.ListedColormap(['mistyrose', 'honeydew', 'lavender'])
        plot_step = 0.02

        # We only take the two corresponding features
        X = iris.data[:, pair]
        y = iris.target

        # Train
        clf = sklearn.base.clone(model)
        clf.fit(X, y)

        
        # Plot the decision boundary
        plt.subplot(2, 3, pairidx + 1)

        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, plot_step),
                             np.arange(y_min, y_max, plot_step))

        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        cs = plt.contourf(xx, yy, Z, cmap= cmap)

        plt.xlabel(iris.feature_names[pair[0]])
        plt.ylabel(iris.feature_names[pair[1]])
        plt.axis("tight")

        # Plot the training points
        for i, color in zip(range(n_classes), plot_colors):
            idx = np.where(y == i)
            plt.scatter(X[idx, 0], X[idx, 1], c=color, label=iris.target_names[i],
                        cmap=plt.cm.Paired, s=5, alpha = 0.8)

        plt.axis("tight")

    plt.suptitle("Decision surface using paired features")
    plt.legend()
    plt.show()

    
    
def plot_confusion_matrix(cm, class_labels,url_dir=""):
    """Pretty prints a confusion matrix as a figure

    Args:
        cm:  A confusion matrix for example
        [[245, 5 ], 
         [ 34, 245]]
         
        class_labels: The list of class labels to be plotted on x-y axis

    Rerturns:
        Just plots the confusion matrix.
    """
    
    df_cm = pd.DataFrame(cm, index = [i for i in class_labels],
                  columns = [i for i in class_labels])
    sns.set(font_scale=1)
    sns.heatmap(df_cm, annot=True, fmt='g', cmap='Blues')
    plt.xlabel("Predicted label")
    plt.ylabel("Real label")
    #plt.show()
    if not url_dir:
        plt.show()
    else:
        plt.savefig(url_dir+'confusion_matrix.png', bbox_inches='tight')
        plt.close()
        
    
    
from sklearn.metrics import roc_curve, roc_auc_score
def get_auc(y, y_pred_probabilities, class_labels, column =1, plot = True):
    fpr, tpr, _ = roc_curve(y == column, y_pred_probabilities[:,column])
    roc_auc = roc_auc_score(y_true=y, y_score=y_pred_probabilities[:,1])
    print ("AUC: ", roc_auc)
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()

import random
def plot_digits_sample(images, target, labels = None):
    # The data that we are interested in is made of 8x8 images of digits, let's
    # have a look at the first images, stored in the `images` attribute of the
    # dataset.  If we were working from image files, we could load them using
    # matplotlib.pyplot.imread.  Note that each image must have the same size. For these
    # images, we know which digit they represent: it is given in the 'target' of
    # the dataset.
    

    fig, axes = plt.subplots(5, 5, figsize=(5, 5),
                             subplot_kw={'xticks':[], 'yticks':[]},
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))

    for i, ax in enumerate(axes.flat):
        im = random.randint(0, len(images)-1)
        ax.imshow(images[im].reshape([8,8]), cmap=plt.cm.gray_r, interpolation='nearest')
        ax.text(0.05, 0.05, str(target[im]),
                transform=ax.transAxes, color='green')

    plt.show()
    

def reduce_mem_usage(df):
    """ iterate through all the columns of a dataframe and modify the data type
        to reduce memory usage.        
    """
    start_mem = df.memory_usage().sum() / 1024**2
    print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))
    
    for col in df.columns:
        col_type = df[col].dtype
        
        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        #else:
        #    df[col] = df[col].astype('category')

    end_mem = df.memory_usage().sum() / 1024**2
    print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
    print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))
    
    return df
      