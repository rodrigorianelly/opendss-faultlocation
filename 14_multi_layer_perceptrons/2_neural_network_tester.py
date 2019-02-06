from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix

import sqlite3
import numpy as np
import pickle

def main():

    filename = 'fault_loc_noPV.sav'
    mlp = pickle.load(open(filename, 'rb'))

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

    # Show results
    predictions = mlp.predict(X_test)
    print('Confusion matrix:\n')
    print(confusion_matrix(y_test,predictions))
    print()
    print(classification_report(y_test,predictions))
    print()
    print(mlp)

if __name__ == "__main__":

    print(
    """
This code can be used to print the neural networks performance. The fault
location neural network for ckt24 without PVSystems is used as an example.
In order to avoid memory errors, it may or may not be necessary to change
test_size.
    """
    )

    main()
