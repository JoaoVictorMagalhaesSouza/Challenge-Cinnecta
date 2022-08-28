from sklearn.cluster import KMeans
import pandas as pd
from copy import deepcopy
from sklearn.preprocessing import LabelEncoder

class DataIntelligence():
    def __init__(self, input_data: pd.DataFrame):
        self.data = deepcopy(input_data)

    def create_clusters(self):
        '''
            My objetive is create a 3 clusters (Customers) from the input_data
        '''
        auxiliar_dataframe = self.data.loc[:,['Description','CustomerID']]
        le1 = LabelEncoder()
        auxiliar_dataframe['Description'] = auxiliar_dataframe['Description'].astype('str')
        auxiliar_dataframe['Description'] = le1.fit_transform(auxiliar_dataframe['Description'])
        le2 = LabelEncoder()
        auxiliar_dataframe['CustomerID'] = auxiliar_dataframe['CustomerID'].astype('str')
        auxiliar_dataframe['CustomerID'] = le2.fit_transform(auxiliar_dataframe['CustomerID'])
        kmeans = KMeans(n_clusters=5,random_state=42).fit(auxiliar_dataframe)
        
        