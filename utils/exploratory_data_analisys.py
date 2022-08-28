import plotly.express as px
import pandas as pd
from copy import deepcopy

class EDA():
    '''
        The goal of this Class is create visualizations
        from question 1 of challenge 
    '''
    def __init__(self, input_data: pd.DataFrame):
        self.data = deepcopy(input_data)
        self.output_data = deepcopy(input_data)
    
    def overview_data (self):
        step = 'DATA OVERVIEW'
        print(f"{[step]} Getting an overview of the data...")
        '''
            View a introdutory overview of the input data
        '''
        print(self.data.info())
        print('\n\n')

    def data_treatment(self):
        step = 'DATA TREATMENT'
        print(f"[{step}] Starting Data Preparation...")
        print(f"[{step}] Initially, we have {len(self.output_data)} rows...")
        '''
            1) Invoices that UnitPrice < 0
                => I saw that they had products with < 0. I went through this phenomenon and
                discovered that the price of a sale of products in analysis is not known, 
                but a debit of analysis, or ours that does not make much sense for analysis.
                So I decided to remove these records !
        '''

        print(f"    => Removing records that UnitPrice < 0...")
        self.output_data = self.output_data[self.output_data['UnitPrice'] >= 0]

        '''
            2) Invoices that UnitPrice=0 and without Description
                => I consider that this cases are irrelevant information for this analisys 
        '''

        print(f"    => Removing records that UnitPrice is 0 and without Description...")
        self.output_data = self.output_data[~(self.output_data['CustomerID'].isnull() & self.output_data['Description'].isnull())]
        '''
            3) Unknown CustomerID
                => The database have many NAs in CustomerID. I don't can drop them,
                because that might be a plausible event. In this case, In this case, I will 
                just explain that the buyer is unknown.
        '''

        print(f"    => Replacing records that don't have a CustomerID...")
        self.output_data['CustomerID'] = self.output_data['CustomerID'].fillna('Unknown')
        
        
        print(f"[{step}] After the treatment, we have {len(self.output_data)} rows...")
        print('\n\n')
        return self.output_data
    
    def question_1a(self,n_best_customers = 10):
        '''
            Input: 
                n_best_customers: the number of best customers that will be viewed
            My objetive:
                => How to define the best clients ?
                    1) Which brought the most money (Quantity x UnitPrice)
                
        '''
        #Getting only the relevant columns for this analisys
        auxiliar_dataframe = self.output_data.loc[:,['Quantity','UnitPrice','CustomerID']]
        #Creating a new feature InvoiceTotal
        auxiliar_dataframe['InvoiceTotal'] = auxiliar_dataframe['Quantity']*auxiliar_dataframe['UnitPrice'] 
        auxiliar_dataframe = auxiliar_dataframe.loc[:,['CustomerID','InvoiceTotal']]
        #Grouping by CustomerID and adding the InvoiceTotal
        best_clients = auxiliar_dataframe.groupby('CustomerID').sum()
        #Doing an accurate customer analysis (Unknown don't is accurate)
        best_clients = best_clients[best_clients.index != 'Unknown']
        best_clients = best_clients.sort_values(by='InvoiceTotal',ascending=False).head(n_best_customers)
        #Plot
        plot = px.pie(best_clients,values='InvoiceTotal',names=best_clients.index, hole=.2,
                        title=f'Best {n_best_customers} customers of the store')
        
        plot.update_traces(textinfo='value')
        plot.show()
        plot.write_image('figures/1a.png')
        
    def question_1b(self,n_best_products = 10):
        '''
            My objetive:
                => How to define the best products ?
                    1) Best seller !
                
        '''
        auxiliar_dataframe = self.output_data.loc[:,['Quantity','Description']]
        best_products = auxiliar_dataframe.groupby('Description').sum().sort_values(by='Quantity',ascending=False).head(n_best_products)
        plot = px.pie(best_products,values='Quantity',names=best_products.index,
                        title=f'Best {n_best_products} products of the store',hole=.2)
        plot.update_traces(textinfo='value')
        plot.show()
        plot.write_image('figures/1b.png')
    
    def question_1c(self):
       #First we go adapt the date column
        auxiliar_dataframe = self.output_data.loc[:,['Description','Quantity','InvoiceDate','UnitPrice']]
        auxiliar_dataframe['InvoiceDate'] = auxiliar_dataframe['InvoiceDate'].dt.strftime('%Y-%m-%d') 
        '''
            Volume
        '''
        volume = auxiliar_dataframe.loc[:,['Quantity','InvoiceDate']].groupby('InvoiceDate').sum()
        volume.index = pd.to_datetime(volume.index)
        volume = volume.sort_index(ascending=True)
        #Plot
        plot = px.bar(volume,x=volume.index,y='Quantity',
                    labels={'Quantity':'Units Sold',
                            'InvoiceDate':'Date'},
                    title=f'Temporal behavior of sales'
        
        )
        plot.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
        plot.update_xaxes(categoryorder='array',categoryarray=volume.index.values)
        plot.update_traces(textinfo='value')
        plot.show()
        plot.write_image('figures/1c_volumes.png')
        '''
            Faturamento
        '''
        invoicing = auxiliar_dataframe.loc[:,['Quantity','UnitPrice','InvoiceDate']]
        invoicing['InvoiceTotal'] = invoicing['Quantity']*invoicing['UnitPrice'] 
        invoicing = invoicing.groupby('InvoiceDate').sum().sort_index(ascending=False)
        invoicing.index = pd.to_datetime(invoicing.index)
        invoicing = invoicing.sort_index(ascending=True)
        #Plot
        plot = px.bar(invoicing,x=invoicing.index,y='InvoiceTotal',
                    labels={'InvoiceTotal':'Invoice Total',
                            'InvoiceDate':'Date'},
                    title=f'Temporal behavior of invoice'
        
        )
        plot.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
        plot.update_xaxes(categoryorder='array',categoryarray=invoicing.index.values)
        plot.update_traces(textinfo='value')
        plot.show()
        plot.write_image('figures/1c_invoice.png')

        '''
            Products
        '''
        products = auxiliar_dataframe.loc[:,['Description','Quantity','InvoiceDate']]
        products = products.groupby(['InvoiceDate','Description']).sum()
        top_3_products_per_day = products.sort_index(ascending=[1,0]).groupby(level=0, as_index=False).apply(lambda x: x.sort_values(by='Quantity',ascending=False).head(3) if len(x) >= 3 else x.head(0)).reset_index(level=0, drop=True)
        top_3_products_per_day = top_3_products_per_day.reset_index()
        #Plot
        plot = px.bar(top_3_products_per_day, x="InvoiceDate", y="Quantity", color="Description",
                        labels={'Quantity':'Sold amount',
                            'InvoiceDate':'Date'},
                    title=f'The 3 best selling products each day'
        )
        plot.update_traces(textinfo='value')
        plot.show() 
        plot.write_image('figures/1c_products.png')

    def question_1d(self):
        '''
            General analisys: Total invoices in all countries
        '''
        auxiliar_dataframe = self.output_data.loc[:,['Quantity','Description','UnitPrice','Country']]
        more_invoices = auxiliar_dataframe.loc[:,['Quantity','Country']].groupby('Country').sum().sort_values(by='Quantity',ascending=False)
        
        #Plot
        plot = px.bar(more_invoices,x=more_invoices.index,y='Quantity',
                    labels={'Quantity':'Units Sold',
                            },
                    title=f'Contry comparison'
        
        )
        plot.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
        plot.update_traces(textinfo='value')
        plot.show()
        plot.write_image('figures/1d_general.png')

        '''
            The most sold product in each country
        '''
        products_country = auxiliar_dataframe.loc[:,['Description','Quantity','Country']]
        products_country = products_country.groupby(['Country','Description']).sum()
        best_product_country = products_country.sort_index(ascending=[1,0]).groupby(level=0, as_index=False).apply(lambda x: x.sort_values(by='Quantity',ascending=False).head(1) if len(x) >= 1 else x.head(0)).reset_index(level=0, drop=True)
        best_product_country = best_product_country.reset_index().sort_values(by='Quantity',ascending=False)
        
        plot = px.bar(best_product_country, x="Country", y="Quantity", color="Description",
                        labels={'Quantity':'Sold amount',
                            'Country':'Country'},
                    title=f'The most sold product in each country'
        )
        plot.update_traces(textinfo='value')
        plot.show() 
        plot.write_image('figures/1d_by_country.png')