# import des librairies dont nous aurons besoin
import pandas as pd
import numpy as np
import re

data = pd.read_csv('linkList.csv')
nb_na = data.isnull().sum()
print(nb_na)