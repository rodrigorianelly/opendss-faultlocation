from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix

import numpy as np
import random
import sqlite3
import pickle

def main():

    conn = sqlite3.connect('database_faultlocation_339PV_round3_6zones.db')
    c = conn.cursor()

    c.execute("""SELECT Vsub_mag1, Vsub_ang1, Vsub_mag2, Vsub_ang2,
        Vsub_mag3, Vsub_ang3, Isub_mag1, Isub_ang1, Isub_mag2,
        Isub_ang2, Isub_mag3, Isub_ang3 FROM PV339_faultloc_db""")

    X = c.fetchall()

    c.execute('SELECT zone FROM PV339_faultloc_db')
    y = c.fetchall()
    y = np.ravel(y)

    # # Take a smaller dataset for tests
    # mix = list(zip(X, y))
    # random.Random(4).shuffle(mix)
    # X, y = zip(*mix)
    # X = X[0:20000]
    # y = y[0:20000]


    X = StandardScaler().fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)

    # hidden layer melhor: (100,100,100,100,100,100)
    n_iter_no_change = 15
    mlp = MLPClassifier(hidden_layer_sizes=(100,100,100,100,100,100),max_iter=1,
           activation='relu', alpha=0.01, batch_size=300, beta_1=0.9,
           beta_2=0.999, early_stopping=False, epsilon=1e-8,
           learning_rate='constant', learning_rate_init=0.001, random_state=7,
           solver='adam', tol=0.0001, shuffle=True, verbose=True,
           warm_start=True, n_iter_no_change=n_iter_no_change)

    mlp.fit(X_train,y_train)

    max_iter = 0
    filename = 'fault_loc_339PV.sav'

    while mlp._no_improvement_count <= n_iter_no_change and max_iter <= 1000:
        mlp.fit(X_train,y_train)
        pickle.dump(mlp, open(filename, 'wb'))
        max_iter = max_iter + 1

    predictions = mlp.predict(X_test)
    print(confusion_matrix(y_test,predictions))
    print(classification_report(y_test,predictions))

if __name__ == "__main__":

    print(
    """
This code makes the classifier to check the fault location. Since it takes a
while to train this network, you can stop running and use the
classifier_fault_location_continuation code to keep running in a posterior
moment.
    """
    )

    main()
