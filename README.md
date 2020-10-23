Hello everyone, my name is Rodrigo Rianelly and this is the code of my 
graduation project!

Here's the abstract:

This work aims to establish the impact of the distributed photovoltaic 
generation on fault location in radial distribution networks. A case study is 
proposed using EPRI ckt24 to do so. Photovoltaic systems are dimensioned for 
this circuit with respect to the penetration limit. Fault simulations are 
performed on OpenDSS in order to acquire voltage and current values at the 
substation. These results are recorded in a database and utilized to train a 
neural network of the multilayer perceptron class, which is capable of 
determining with 90% average success rate the fault location between 6 possible 
geographic regions in the circuit in presence or not of distributed photovoltaic 
generation.

And here are the keywords:
Radial distribution networks. Distributed photovoltaic generation. Photovoltaic 
systems. Penetration limit. OpenDSS. EPRI ckt24. Fault location. Supervised 
learning. Neural network. Multilayer perceptron.

You can look into Fault_location_ckt24.pptx to see a simple graphical 
explanation of the project, or go to TCC_Rodrigo_Rianelly to read the full 
document.

In order to run the codes, you should have Python 3, OpenDSS, a .db reader
and some python packages such as win32com, numpy, matplotlib and sqlite3.

Since it takes a long time to run the fault simulations that build up the
database, I have uploaded the files to Google Drive:
https://drive.google.com/open?id=1jzBDv_J_BDSlXoOs8bTm0COY-eiDCQmk
