#%% Imports
from tkinter import Label
import pandas as pd
from utils import exploratory_data_analisys
from utils import data_intelligence
%load_ext autoreload
%autoreload 2

#%% 1) Read input data
base_data_path = './data/'
name_input_data = 'Engenheiro de Dados - Teste Prático.xlsx'
input_data = pd.read_excel(f"{base_data_path}{name_input_data}")

#%% 2) EDA of the data
eda = exploratory_data_analisys.EDA(input_data)
eda.overview_data()
final_data = eda.data_treatment()
# #%% Test KMeans
# from sklearn.cluster import KMeans
# from sklearn.preprocessing import LabelEncoder
# a = final_data.loc[:,['Description','CustomerID','Country']]
# le1 = LabelEncoder()
# a['Description'] = a['Description'].astype('str')
# a['Description'] = le1.fit_transform(a['Description'])
# le2 = LabelEncoder()
# a['CustomerID'] = a['CustomerID'].astype('str')
# a['CustomerID'] = le2.fit_transform(a['CustomerID'])
# le3 = LabelEncoder()
# a['Country'] = a['Country'].astype('str')
# a['Country'] = le3.fit_transform(a['Country'])

# kmeans = KMeans(n_clusters=3, random_state=0).fit(a)
# a['Group'] = kmeans.labels_
# #group_bag = a[(a['Description'].str.contains('BAG')) & (a['Group']==2)]

# # import plotly.express as px
# # fig = px.scatter(a,x='CustomerID',y='Description',color='Group')
# # fig.show()
# #%%
# import seaborn as sns
# sns.scatterplot(x=a['CustomerID'],y=a['Description'],hue=a['Group'])
# #%%
# a['Description'] = le1.inverse_transform(a['Description'])
# a['CustomerID'] = le2.inverse_transform(a['CustomerID'])
# a['Country'] = le3.inverse_transform(a['Country'])
# #%%
# #Grupo 0
# analise_0 = a[a['Group']==0]
# all_customers = len(final_data['CustomerID'].value_counts())
# #customers_cake = len(analise_0['CustomerID'][analise_0['Description'].str.contains('CAKE')].value_counts())
# customers_cake = len(final_data['CustomerID'][(final_data['Description'].str.contains('CAKE',na=False)) & (final_data['Quantity']>0)].value_counts())
# print(f'{(customers_cake/all_customers)*100}% customers are interested in CAKE products.')

# #%%
# #Grupo 1:
# analise_1 = a[a['Group']==1]
# all_customers = len(final_data['CustomerID'].value_counts())
# #customers_bag = len(analise_1['CustomerID'][analise_1['Description'].str.contains('BAG')].value_counts())
# customers_bag = len(final_data['CustomerID'][(final_data['Description'].str.contains('BAG',na=False)) & (final_data['Quantity']>0)].value_counts())
# print(f'{(customers_bag/all_customers)*100}% customers are interested in BAGs products.')

# #%%
# #Grupo 2:
# analise_2 = a[a['Group']==2]
# all_customers = len(final_data['CustomerID'].value_counts())
# #customers_clock = len(analise_2['CustomerID'][analise_2['Description'].str.contains('CLOCK')].value_counts())
# customers_clock = len(final_data['CustomerID'][(final_data['Description'].str.contains('CLOCK',na=False)) & (final_data['Quantity']>0)].value_counts())
# print(f'{(customers_clock/all_customers)*100}% customers are interested in CLOCK products.')

#%% 3) Question 1-a)
eda.question_1a()
#%% 4) Question 1-b)
eda.question_1b()
#%% 5) Question 1-c)
eda.question_1c()
#%% 6) Question 1-d)
eda.question_1d()
#%% 7) Question 2)
di = data_intelligence.DataIntelligence(final_data)
di.segmentation_clients()
#%%
