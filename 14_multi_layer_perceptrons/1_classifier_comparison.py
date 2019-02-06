from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.metrics import classification_report,confusion_matrix

import numpy as np
import random
import sqlite3
import pickle

def main():

    conn = sqlite3.connect('database_faultlocation_noPV_withzones.db')
    c = conn.cursor()

    c.execute("""SELECT Vsub_mag1, Vsub_ang1, Vsub_mag2, Vsub_ang2,
        Vsub_mag3, Vsub_ang3, Isub_mag1, Isub_ang1, Isub_mag2,
        Isub_ang2, Isub_mag3, Isub_ang3 FROM noPV_faultloc_db""")

    X = c.fetchall()

    c.execute('SELECT zone FROM noPV_faultloc_db')
    y = c.fetchall()
    y = np.ravel(y)

    # Take a smaller dataset for tests
    mix = list(zip(X, y))
    random.shuffle(mix)
    X, y = zip(*mix)
    X = X[0:10000]
    y = y[0:10000]

    X = StandardScaler().fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    print("MLP")
    mlp = MLPClassifier(hidden_layer_sizes=(100,100,100,100,100,100),
           max_iter=2000, activation='relu', alpha=0.01, batch_size=300,
           beta_1=0.9, beta_2=0.999, early_stopping=False, epsilon=1e-8,
           learning_rate='constant', learning_rate_init=0.001, random_state=7,
           solver='adam', tol=0.0001, shuffle=True,
           verbose=False, warm_start=False, n_iter_no_change=15)
    mlp.fit(X_train,y_train)
    pred = mlp.predict(X_test)
    print(classification_report(y_test,pred))

    print("K_nei")
    k_nei = KNeighborsClassifier(n_neighbors=1, weights='uniform',
    algorithm='brute', p=9)
    k_nei.fit(X_train,y_train)
    pred = k_nei.predict(X_test)
    print(classification_report(y_test,pred))

    print("SVM")
    SVM = SVC(C=14, kernel='poly', gamma=5)
    SVM.fit(X_train,y_train)
    pred = SVM.predict(X_test)
    print(classification_report(y_test,pred))

    print("dec_tree")
    dec_tree = DecisionTreeClassifier(criterion='entropy', splitter='best',
    min_samples_split=5, min_samples_leaf=1, max_features=None)
    dec_tree.fit(X_train,y_train)
    pred = dec_tree.predict(X_test)
    print(classification_report(y_test,pred))

    print("rand_forest")
    rand_forest = RandomForestClassifier(n_estimators=50, criterion='entropy',
    min_samples_split=3, min_samples_leaf=1)
    rand_forest.fit(X_train,y_train)
    pred = rand_forest.predict(X_test)
    print(classification_report(y_test,pred))

if __name__ == "__main__":

    print(
    """
This code compares classifiers for a sample of the database of faultlocation 
without PVSystems.
    """
    )

    main()
