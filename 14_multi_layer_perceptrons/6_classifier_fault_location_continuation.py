from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix

import numpy as np
import random
import sqlite3
import pickle

def main():

    conn = sqlite3.connect('database_faultlocation_339PV_withzones.db')
    c = conn.cursor()

    c.execute("""SELECT Vsub_mag1, Vsub_ang1, Vsub_mag2, Vsub_ang2,
        Vsub_mag3, Vsub_ang3, Isub_mag1, Isub_ang1, Isub_mag2,
        Isub_ang2, Isub_mag3, Isub_ang3 FROM PV339_faultloc_db""")

    X = c.fetchall()

    c.execute('SELECT zone FROM PV339_faultloc_db')
    y = c.fetchall()
    y = np.ravel(y)


    X = StandardScaler().fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)

    filename = 'fault_loc_339PV.sav'
    mlp = pickle.load(open(filename, 'rb'))

    # Keep training
    max_iter = 0
    n_iter_no_change = 15
    while mlp._no_improvement_count <= n_iter_no_change and max_iter <= 300:
        mlp.fit(X_train,y_train)
        pickle.dump(mlp, open(filename, 'wb'))
        max_iter = max_iter + 1

    # Show results
    predictions = mlp.predict(X_test)
    print(confusion_matrix(y_test,predictions))
    print(classification_report(y_test,predictions))

if __name__ == "__main__":

    print(
    """
This code takes an existing .sav neural network for fault location and keeps
training it.
    """
    )

    main()
