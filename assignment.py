import mysql.connector
import pandas as pd
import plotly.graph_objects as go

mydb=mysql.connector.connect(host="localhost",user="root",password="root",db="new_schema")
mycursor=mydb.cursor()
mycursor.execute('select customer.CustomerName as customer_name,salesorders.ID as order_id,salesorders.value as order_value from customer LEFT JOIN salesorders ON salesorders.customer_id=customer.ID')
customer_details=mycursor.fetchall()
details=pd.DataFrame(customer_details)
mycursor.execute('select products.product as product_name,orderedunits.order_id as order_id from products LEFT JOIN orderedunits ON products.ID=orderedunits.unit_id where products.product="Electric Motor" or products.product="Tyre"')
product_details=mycursor.fetchall()
product_data=pd.DataFrame(product_details)
data6=details.rename(columns={0:"customer_name",1:"order_id",2:"order_value"})
data7=product_data.rename(columns={0:"product_name",1:"order_id"})
data6=data6.dropna()
data6['order_id'] = data6['order_id'].apply(lambda x: int(x))
final_df=data6.merge(data7, on='order_id', how='left')
final_df.dropna()

x=[final_df.iloc[0]['customer_name']+"="+final_df.iloc[0]['product_name'],final_df.iloc[1]['customer_name']+"="+final_df.iloc[1]['product_name'],final_df.iloc[2]['customer_name']+"="+final_df.iloc[2]['product_name']]
y=[final_df.iloc[0]['order_value'],final_df.iloc[1]['order_value'],final_df.iloc[2]['order_value']]
data=[go.Bar(x=x,y=y)]
layout=go.Layout(title="value of order against customer")
fig = go.Figure(data=data, layout=layout)
fig.show()
