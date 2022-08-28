from sklearn.cluster import KMeans
import pandas as pd
from copy import deepcopy
from sklearn.preprocessing import LabelEncoder
import seaborn as sns

class DataIntelligence():
    def __init__(self, input_data: pd.DataFrame):
        self.data = deepcopy(input_data)

    def segmentation_clients(self):
        '''
            My objetive is create auxiliar_dataframe 3 clusters (Customers) from the input_data
        '''
        auxiliar_dataframe = self.data.loc[:,['Description','CustomerID']]
        le1 = LabelEncoder()
        auxiliar_dataframe['Description'] = auxiliar_dataframe['Description'].astype('str')
        auxiliar_dataframe['Description'] = le1.fit_transform(auxiliar_dataframe['Description'])
        le2 = LabelEncoder()
        auxiliar_dataframe['CustomerID'] = auxiliar_dataframe['CustomerID'].astype('str')
        auxiliar_dataframe['CustomerID'] = le2.fit_transform(auxiliar_dataframe['CustomerID'])
        le3 = LabelEncoder()
        auxiliar_dataframe['Country'] = auxiliar_dataframe['Country'].astype('str')
        auxiliar_dataframe['Country'] = le3.fit_transform(auxiliar_dataframe['Country'])

        kmeans = KMeans(n_clusters=5,random_state=42).fit(auxiliar_dataframe)
        
        auxiliar_dataframe['Group'] = kmeans.labels_
        #View the clusters
        sns.scatterplot(x=auxiliar_dataframe['CustomerID'],y=auxiliar_dataframe['Description'],hue=auxiliar_dataframe['Group'])
        
        auxiliar_dataframe['Description'] = le1.inverse_transform(auxiliar_dataframe['Description'])
        auxiliar_dataframe['CustomerID'] = le2.inverse_transform(auxiliar_dataframe['CustomerID'])
        auxiliar_dataframe['Country'] = le3.inverse_transform(auxiliar_dataframe['Country'])
        
        #Group 0
        analise_0 = auxiliar_dataframe[auxiliar_dataframe['Group']==0]
        all_customers = len(self.data['CustomerID'].value_counts())
        #customers_cake = len(analise_0['CustomerID'][analise_0['Description'].str.contains('CAKE')].value_counts())
        customers_cake = len(self.data['CustomerID'][(self.data['Description'].str.contains('CAKE',na=False)) & (self.data['Quantity']>0)].value_counts())
        print(f'{(customers_cake/all_customers)*100}% customers are interested in CAKE products.')

        #Group 1:
        analise_1 = auxiliar_dataframe[auxiliar_dataframe['Group']==1]
        all_customers = len(self.data['CustomerID'].value_counts())
        #customers_bag = len(analise_1['CustomerID'][analise_1['Description'].str.contains('BAG')].value_counts())
        customers_bag = len(self.data['CustomerID'][(self.data['Description'].str.contains('BAG',na=False)) & (self.data['Quantity']>0)].value_counts())
        print(f'{(customers_bag/all_customers)*100}% customers are interested in BAGs products.')

        #Group 2:
        analise_2 = auxiliar_dataframe[auxiliar_dataframe['Group']==2]
        all_customers = len(self.data['CustomerID'].value_counts())
        #customers_clock = len(analise_2['CustomerID'][analise_2['Description'].str.contains('CLOCK')].value_counts())
        customers_clock = len(self.data['CustomerID'][(self.data['Description'].str.contains('CLOCK',na=False)) & (self.data['Quantity']>0)].value_counts())
        print(f'{(customers_clock/all_customers)*100}% customers are interested in CLOCK products.')
