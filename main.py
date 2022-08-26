#%% Imports
import pandas as pd
from utils import exploratory_data_analisys
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
#%% 3) Question 1-a)
eda.question_1a()
#%% 4) Question 1-b)
eda.question_1b()
#%% 5) Question 1-c)
eda.question_1c()
#%% 6) Question 1-d)
eda.question_1d()

# %%
