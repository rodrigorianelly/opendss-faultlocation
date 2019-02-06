from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import balanced_accuracy_score

import numpy as np
import random
import sqlite3
import pickle
import json

def float3(data):
    data = round(float(data),3)
    return data

def main():

    conn = sqlite3.connect('database_faultlocation_339PV_withzones.db')
    c = conn.cursor()

    c.execute("""SELECT Vsub_mag1, Vsub_ang1, Vsub_mag2, Vsub_ang2,
        Vsub_mag3, Vsub_ang3, Isub_mag1, Isub_ang1, Isub_mag2,
        Isub_ang2, Isub_mag3, Isub_ang3 FROM PV339_faultloc_db""")

    X = c.fetchall()
    random.shuffle(X)
    X_test = X[:10000]
    X = X[1000000:]

    y = ['fault' for i in range(len(X))]
    y_test = ['fault' for i in range(len(X_test))]

    j = 2
    for line in open("ckt24_manyPV_solve.txt", "r"):
        data = json.loads(line)
        results_x = (float3(data[2][0]),
        float3(data[2][1]), float3(data[2][2]), float3(data[2][3]),
        float3(data[2][4]), float3(data[2][5]), float3(data[4][8]),
        float3(data[4][9]), float3(data[4][10]), float3(data[4][11]),
        float3(data[4][12]), float3(data[4][13]))
        if j%2==0:
            X.append(results_x)
            y.append('no fault')
            j = j+1

        elif j%2==1:
            X_test.append(results_x)
            y_test.append('no fault')
            j = j+1



    X = StandardScaler().fit_transform(X)
    X_test = StandardScaler().fit_transform(X_test)

    ros = RandomOverSampler(random_state=0)
    X_resampled, y_resampled = ros.fit_resample(X, y)

    # # #Take a smaller dataset for tests
    # # mix = list(zip(X_resampled, y_resampled))
    # # random.shuffle(mix)
    # # X_resampled, y_resampled = zip(*mix)
    # # X_resampled = X_resampled[0:10000]
    # # y_resampled = y_resampled[0:10000]

    n_iter_no_change = 15
    mlp = MLPClassifier(hidden_layer_sizes=(30,30,30),max_iter=1,
           activation='relu', alpha=0.01, batch_size=300, beta_1=0.9,
           beta_2=0.999, early_stopping=False, epsilon=1e-8,
           learning_rate='constant', learning_rate_init=0.001, random_state=7,
           solver='adam', tol=0.0001, shuffle=True, verbose=True,
           warm_start=True, n_iter_no_change=15)

    mlp.fit(X_resampled,y_resampled)

    filename = 'fault_detec_339PV.sav'

    max_iter = 0
    while mlp._no_improvement_count <= n_iter_no_change and max_iter <= 500:
        mlp.fit(X_resampled,y_resampled)
        pickle.dump(mlp, open(filename, 'wb'))
        max_iter = max_iter + 1

    mlp.fit(X_resampled,y_resampled)
    predictions = mlp.predict(X_test)

    print(confusion_matrix(y_test,predictions))
    # print(classification_report(y_test,predictions))
    print(balanced_accuracy_score(y_test, predictions, sample_weight=None,
    adjusted=False))

if __name__ == "__main__":

    print(
    """
This code makes the classifier to check if there is or not a fault situation
based on currents and voltages in the substation transformer.
    """
    )

    main()
