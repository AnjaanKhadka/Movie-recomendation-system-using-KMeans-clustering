import numpy as np
from matplotlib.pyplot import plot
import pre_processing


label = ['P_Genre','S_Genre','T_Genre']
u_labels = np.unique(label)
df = pre_processing.pre_process_all()
#plotting the results:
 

 
for i in u_labels:
    plot.scatter(df[label == i , 0] , df[label == i , 1] , label = i)
plot.legend()
plot.show()